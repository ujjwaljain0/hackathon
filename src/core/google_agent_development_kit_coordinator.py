"""Coordinator following the Google Agent Development Kit style using LiteLLM.

This coordinator exposes LLM tool-calling for Jira and Confluence tools backed
by the existing MCP-based agents.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

from litellm import completion
from .llm_agent import LlmAgent, LiteLlm

from .types import AgentResponse, Command, CommandType
from ..agents.jira_agent import JiraAgent
from ..agents.confluence_agent import ConfluenceAgent

logger = logging.getLogger(__name__)


class GoogleAgentDevelopmentKitCoordinator:
    """LiteLLM-powered coordinator that mirrors Google Agent Development Kit patterns."""

    def __init__(
        self,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
    ) -> None:
        self.model = model or os.getenv("LITELLM_MODEL", "openai/gpt-4o-mini")
        self.system_prompt = system_prompt or (
            "You are an orchestration agent for project management. "
            "Use the provided tools to operate Jira and Confluence. "
            "Prefer precise function calls over prose.")

        self.jira_agent = JiraAgent(os.getenv("JIRA_MCP_URL", "https://athonprompt.atlassian.net/rest/api/3"))
        self.confluence_agent = ConfluenceAgent(os.getenv("CONFLUENCE_MCP_URL", "https://athonprompt.atlassian.net/wiki/rest/api"))

        self.tools: List[Dict[str, Any]] = [
            {
                "type": "function",
                "function": {
                    "name": "jira_get_issues",
                    "description": "Retrieve Jira issues with optional filters",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "project": {"type": "string"},
                            "status": {"type": "string"},
                            "assignee": {"type": "string"},
                            "issue_type": {"type": "string"},
                            "max_results": {"type": "integer", "default": 50},
                        },
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "jira_create_issue",
                    "description": "Create a new Jira issue",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "project": {"type": "string"},
                            "summary": {"type": "string"},
                            "description": {"type": "string"},
                            "issue_type": {"type": "string", "default": "Task"},
                            "priority": {"type": "string", "default": "Medium"},
                            "assignee": {"type": "string"},
                            "labels": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": ["project", "summary"],
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "jira_update_issue",
                    "description": "Update an existing Jira issue by key",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "issue_key": {"type": "string"},
                            "updates": {"type": "object"},
                        },
                        "required": ["issue_key", "updates"],
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "confluence_get_page",
                    "description": "Retrieve a Confluence page by id/title/space",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "page_id": {"type": "string"},
                            "title": {"type": "string"},
                            "space_key": {"type": "string"},
                        },
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "confluence_create_page",
                    "description": "Create a Confluence page",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "content": {"type": "string"},
                            "space_key": {"type": "string"},
                            "parent_id": {"type": "string"},
                            "labels": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": ["title", "content", "space_key"],
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "confluence_update_page",
                    "description": "Update a Confluence page",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "page_id": {"type": "string"},
                            "updates": {"type": "object"},
                        },
                        "required": ["page_id", "updates"],
                        "additionalProperties": False,
                    },
                },
            },
        ]

    async def initialize(self) -> bool:
        jira_ok = await self.jira_agent.initialize()
        confluence_ok = await self.confluence_agent.initialize()
        
        # Initialize LLM agent matching requested style
        self.llm_agent = LlmAgent(
            name="project_orchestrator",
            model=LiteLlm(
                model=self.model,
                api_base=os.getenv("LITELLM_API_BASE"),
                api_key=os.getenv("LITELLM_API_KEY"),
            ),
            system_prompt=self.system_prompt,
        )
        
        # Store connection status for graceful degradation
        self.jira_available = jira_ok
        self.confluence_available = confluence_ok
        
        # Return True if LLM is available (coordinator can work with just LLM)
        return True

    async def shutdown(self) -> None:
        await self.jira_agent.shutdown()
        await self.confluence_agent.shutdown()

    async def chat_execute(self, user_message: str) -> List[AgentResponse]:
        logger.info(f"🤖 AI Processing request: {user_message[:100]}...")
        
        resp = self.llm_agent.chat(user_message=user_message, tools=self.tools)
        msg = resp.choices[0].message  # type: ignore[index]

        tool_calls = getattr(msg, "tool_calls", None)
        if tool_calls:
            logger.info(f"🔧 AI selected {len(tool_calls)} tool(s) to execute")
            results: List[AgentResponse] = []
            for tool_call in tool_calls:
                name = tool_call.function.name  # type: ignore[attr-defined]
                args = tool_call.function.arguments  # type: ignore[attr-defined]
                import json

                try:
                    parsed_args = json.loads(args) if isinstance(args, str) else (args or {})
                    logger.info(f"🛠️  Executing tool: {name}")
                    data = await self._invoke_tool(name, parsed_args)
                    # Check if tool returned an error
                    if isinstance(data, dict) and data.get("status") in ["unavailable", "error"]:
                        logger.error(f"❌ Tool failed: {name} - {data.get('error')}")
                        results.append(AgentResponse(agent_name=name, success=False, data=data, error_message=data.get("error")))
                    else:
                        logger.info(f"✅ Tool completed successfully: {name}")
                        # Log summary of what was created/updated
                        self._log_tool_result_summary(name, data)
                        results.append(AgentResponse(agent_name=name, success=True, data=data))
                except Exception as e:
                    logger.error(f"❌ Tool exception: {name} - {str(e)}")
                    results.append(AgentResponse(agent_name=name, success=False, data=None, error_message=str(e)))
            return results

        logger.info("💬 AI provided text response (no tools used)")
        return [AgentResponse(agent_name="llm", success=True, data=getattr(msg, "content", ""))]

    async def execute_command(self, command: Command) -> List[AgentResponse]:
        if command.command_type in {CommandType.JIRA_ISSUE, CommandType.JIRA_PROJECT, CommandType.JIRA_SPRINT}:
            return [
                AgentResponse(
                    agent_name="jira",
                    success=True,
                    data=await self._execute_jira(command.action, command.parameters),
                )
            ]
        if command.command_type in {CommandType.CONFLUENCE_PAGE, CommandType.CONFLUENCE_SPACE}:
            return [
                AgentResponse(
                    agent_name="confluence",
                    success=True,
                    data=await self._execute_confluence(command.action, command.parameters),
                )
            ]
        return await self.chat_execute(f"Execute command: {command}")

    def _log_tool_result_summary(self, tool_name: str, data: Any) -> None:
        """Log a high-level summary of what was created/updated."""
        try:
            if tool_name == "jira_create_issue" and hasattr(data, 'key'):
                logger.info(f"📊 CREATION SUMMARY - Jira Issue: {data.key} ({data.summary})")
            elif tool_name == "jira_update_issue" and hasattr(data, 'key'):
                logger.info(f"📊 UPDATE SUMMARY - Jira Issue: {data.key} ({data.summary})")
            elif tool_name == "confluence_create_page" and hasattr(data, 'id'):
                logger.info(f"📊 CREATION SUMMARY - Confluence Page: {data.title} (ID: {data.id})")
            elif tool_name == "confluence_update_page" and hasattr(data, 'id'):
                logger.info(f"📊 UPDATE SUMMARY - Confluence Page: {data.title} (ID: {data.id})")
            elif tool_name == "jira_get_issues" and isinstance(data, list):
                logger.info(f"📊 QUERY SUMMARY - Found {len(data)} Jira issue(s)")
            elif tool_name == "confluence_get_page" and data:
                logger.info(f"📊 QUERY SUMMARY - Retrieved Confluence page: {getattr(data, 'title', 'Unknown')}")
        except Exception as e:
            logger.debug(f"Failed to log tool result summary: {e}")

    async def _invoke_tool(self, name: str, args: Dict[str, Any]) -> Any:
        try:
            if name.startswith("jira_"):
                if not self.jira_available:
                    return {"error": "Jira MCP server not available", "status": "unavailable"}
                if name == "jira_get_issues":
                    return await self.jira_agent.get_issues(**args)
                if name == "jira_create_issue":
                    return await self.jira_agent.create_issue(**args)
                if name == "jira_update_issue":
                    return await self.jira_agent.update_issue(**args)
            elif name.startswith("confluence_"):
                if not self.confluence_available:
                    return {"error": "Confluence MCP server not available", "status": "unavailable"}
                if name == "confluence_get_page":
                    return await self.confluence_agent.get_page(**args)
                if name == "confluence_create_page":
                    return await self.confluence_agent.create_page(**args)
                if name == "confluence_update_page":
                    return await self.confluence_agent.update_page(**args)
            raise ValueError(f"Unknown tool: {name}")
        except Exception as e:
            return {"error": str(e), "status": "error"}

    async def _execute_jira(self, action: str, params: Dict[str, Any]) -> Any:
        if action == "get_issues":
            return await self.jira_agent.get_issues(**params)
        if action == "create_issue":
            return await self.jira_agent.create_issue(**params)
        if action == "update_issue":
            return await self.jira_agent.update_issue(**params)
        raise ValueError(f"Unknown Jira action: {action}")

    async def _execute_confluence(self, action: str, params: Dict[str, Any]) -> Any:
        if action == "get_page":
            return await self.confluence_agent.get_page(**params)
        if action == "create_page":
            return await self.confluence_agent.create_page(**params)
        if action == "update_page":
            return await self.confluence_agent.update_page(**params)
        raise ValueError(f"Unknown Confluence action: {action}")


