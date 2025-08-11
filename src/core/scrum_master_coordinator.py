"""Scrum Master coordinator for Google Agent Development Kit web interface."""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

from .llm_agent import LlmAgent, LiteLlm
from .types import AgentResponse
from ..agents.scrum_master_agent import ScrumMasterAgent

logger = logging.getLogger(__name__)


class ScrumMasterCoordinator:
    """
    Google Agent Development Kit coordinator specifically for Scrum Master operations.
    Integrates with 'adk web' interface to provide AI-powered scrum master capabilities.
    """

    def __init__(
        self,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
    ) -> None:
        self.model = model or os.getenv("LITELLM_MODEL", "openai/gpt-4o-mini")
        self.system_prompt = system_prompt or (
            "You are an experienced Scrum Master AI assistant. "
            "You help teams with sprint planning, task assignment, daily standups, "
            "backlog grooming, and sprint retrospectives. You use Jira for issue "
            "management and Confluence for documentation. "
            
            "IMPORTANT: You MUST ask users to provide their Jira project key and "
            "Confluence space key before performing any actions. These are required "
            "parameters for all operations. Never assume or hardcode these values. "
            
            "When users request sprint operations, politely ask them to specify: "
            "1. Their Jira project key (e.g., 'PROJ', 'DEV', 'TEAM') "
            "2. Their Confluence space key (e.g., 'DEV', 'TEAM', 'DOCS') "
            
            "You focus on team productivity, removing blockers, and ensuring smooth "
            "sprint execution. Always think like a real Scrum Master - be proactive, "
            "supportive, and focused on continuous improvement."
        )

        # Initialize the Scrum Master agent
        self.scrum_master = ScrumMasterAgent()
        
        # Define tools available to the AI
        self.tools: List[Dict[str, Any]] = [
            # Sprint Management Tools
            {
                "type": "function",
                "function": {
                    "name": "start_sprint",
                    "description": "Start a new sprint with planning and documentation",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sprint_name": {"type": "string", "description": "Name of the sprint (e.g., 'Sprint 1', 'Q1 Sprint 3')"},
                            "duration_weeks": {"type": "integer", "default": 2, "description": "Sprint duration in weeks"},
                            "sprint_goal": {"type": "string", "description": "Main goal/objective for this sprint"},
                            "jira_project_key": {"type": "string", "description": "Jira project key (user must specify)"},
                            "confluence_space_key": {"type": "string", "description": "Confluence space key for documentation (user must specify)"},
                        },
                        "required": ["sprint_name", "sprint_goal", "jira_project_key", "confluence_space_key"],
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "plan_sprint",
                    "description": "Conduct sprint planning session with requirements and team",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "requirements": {
                                "type": "array",
                                "description": "List of requirements/user stories for the sprint",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string"},
                                        "description": {"type": "string"},
                                        "priority": {"type": "string", "enum": ["Low", "Medium", "High", "Critical"]},
                                        "estimated_hours": {"type": "integer"},
                                        "required_skills": {"type": "array", "items": {"type": "string"}},
                                    }
                                }
                            },
                            "team_members": {
                                "type": "array",
                                "description": "Team members available for the sprint",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "username": {"type": "string"},
                                        "display_name": {"type": "string"},
                                        "skills": {"type": "array", "items": {"type": "string"}},
                                        "capacity": {"type": "number", "description": "Work capacity (0.0-1.0)"},
                                    }
                                }
                            },
                            "sprint_capacity": {"type": "integer", "default": 40, "description": "Total sprint capacity in story points"},
                            "jira_project_key": {"type": "string", "description": "Jira project key for creating issues"},
                        },
                        "required": ["requirements", "team_members", "jira_project_key"],
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "conduct_standup",
                    "description": "Conduct daily standup meeting and provide status update",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "jira_project_key": {"type": "string", "description": "Jira project key to check issues"},
                        },
                        "required": ["jira_project_key"],
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "assign_tasks",
                    "description": "Intelligently assign tasks to team members based on skills and workload",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "requirements": {
                                "type": "array",
                                "description": "Tasks/requirements to assign",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string"},
                                        "description": {"type": "string"},
                                        "priority": {"type": "string"},
                                        "issue_type": {"type": "string", "default": "Task"},
                                        "estimated_hours": {"type": "integer"},
                                        "required_skills": {"type": "array", "items": {"type": "string"}},
                                    }
                                }
                            },
                            "team_members": {
                                "type": "array",
                                "description": "Available team members",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "username": {"type": "string"},
                                        "display_name": {"type": "string"},
                                        "skills": {"type": "array", "items": {"type": "string"}},
                                        "capacity": {"type": "number"},
                                    }
                                }
                            },
                            "jira_project_key": {"type": "string", "description": "Jira project key for creating issues"},
                        },
                        "required": ["requirements", "team_members", "jira_project_key"],
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_burndown",
                    "description": "Generate burndown chart data for current sprint",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "jira_project_key": {"type": "string", "description": "Jira project key for burndown analysis"},
                        },
                        "required": ["jira_project_key"],
                        "additionalProperties": False,
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "sprint_report",
                    "description": "Generate comprehensive sprint status report",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "jira_project_key": {"type": "string", "description": "Jira project key for sprint report"},
                            "include_team_metrics": {"type": "boolean", "default": True},
                        },
                        "required": ["jira_project_key"],
                        "additionalProperties": False,
                    },
                },
            },
        ]

    async def initialize(self) -> bool:
        """Initialize the Scrum Master coordinator."""
        scrum_master_ok = await self.scrum_master.initialize()
        
        if scrum_master_ok:
            # Initialize LLM agent
            self.llm_agent = LlmAgent(
                name="scrum_master_ai",
                model=LiteLlm(
                    model=self.model,
                    api_base=os.getenv("LITELLM_API_BASE"),
                    api_key=os.getenv("LITELLM_API_KEY"),
                ),
                system_prompt=self.system_prompt,
            )
            logger.info("✅ Scrum Master Coordinator initialized successfully")
        else:
            logger.warning("⚠️ Scrum Master Coordinator initialized with limited functionality")
        
        return scrum_master_ok

    async def shutdown(self) -> None:
        """Shutdown the coordinator."""
        await self.scrum_master.shutdown()

    async def chat_execute(self, user_message: str) -> List[AgentResponse]:
        """Execute user requests through AI tool calling."""
        logger.info(f"🏃‍♂️ Scrum Master AI processing: {user_message[:100]}...")
        
        try:
            resp = self.llm_agent.chat(user_message=user_message, tools=self.tools)
            msg = resp.choices[0].message  # type: ignore[index]

            tool_calls = getattr(msg, "tool_calls", None)
            if tool_calls:
                logger.info(f"🔧 Scrum Master AI selected {len(tool_calls)} action(s)")
                results: List[AgentResponse] = []
                
                for tool_call in tool_calls:
                    name = tool_call.function.name  # type: ignore[attr-defined]
                    args = tool_call.function.arguments  # type: ignore[attr-defined]
                    import json

                    try:
                        parsed_args = json.loads(args) if isinstance(args, str) else (args or {})
                        logger.info(f"🛠️ Executing Scrum Master action: {name}")
                        
                        data = await self._invoke_scrum_action(name, parsed_args)
                        
                        if isinstance(data, dict) and data.get("error"):
                            results.append(AgentResponse(
                                agent_name=f"scrum_master_{name}", 
                                success=False, 
                                data=data, 
                                error_message=data.get("error")
                            ))
                        else:
                            logger.info(f"✅ Scrum Master action completed: {name}")
                            results.append(AgentResponse(
                                agent_name=f"scrum_master_{name}", 
                                success=True, 
                                data=data
                            ))
                    except Exception as e:
                        logger.error(f"❌ Scrum Master action failed: {name} - {str(e)}")
                        results.append(AgentResponse(
                            agent_name=f"scrum_master_{name}", 
                            success=False, 
                            data=None, 
                            error_message=str(e)
                        ))
                
                return results

            # If no tools called, return AI response
            logger.info("💬 Scrum Master provided advisory response")
            return [AgentResponse(
                agent_name="scrum_master_advisor", 
                success=True, 
                data=getattr(msg, "content", "")
            )]
        
        except Exception as e:
            logger.error(f"❌ Scrum Master AI error: {str(e)}")
            return [AgentResponse(
                agent_name="scrum_master_error", 
                success=False, 
                data=None, 
                error_message=str(e)
            )]

    async def _invoke_scrum_action(self, action_name: str, args: Dict[str, Any]) -> Any:
        """Invoke Scrum Master actions."""
        try:
            if action_name == "start_sprint":
                return await self.scrum_master.start_sprint(**args)
            elif action_name == "plan_sprint":
                return await self.scrum_master.plan_sprint(**args)
            elif action_name == "conduct_standup":
                return await self.scrum_master.conduct_standup(**args)
            elif action_name == "assign_tasks":
                return await self.scrum_master.assign_tasks(**args)
            elif action_name == "generate_burndown":
                return await self.scrum_master.generate_burndown(**args)
            elif action_name == "sprint_report":
                # Create a comprehensive sprint report
                standup_data = await self.scrum_master.conduct_standup(**args)
                burndown_data = await self.scrum_master.generate_burndown(**args)
                
                return {
                    "sprint_status": standup_data,
                    "burndown_metrics": burndown_data,
                    "generated_at": "2025-01-11",
                    "scrum_master_recommendations": self._generate_recommendations(standup_data, burndown_data)
                }
            else:
                raise ValueError(f"Unknown Scrum Master action: {action_name}")
        
        except Exception as e:
            logger.error(f"❌ Scrum Master action execution error: {str(e)}")
            return {"error": str(e)}

    def _generate_recommendations(self, standup_data: Dict[str, Any], burndown_data: Dict[str, Any]) -> List[str]:
        """Generate Scrum Master recommendations based on sprint data."""
        recommendations = []
        
        if isinstance(standup_data, dict):
            blocked_count = len(standup_data.get("blocked_issues", []))
            if blocked_count > 0:
                recommendations.append(f"🚫 Address {blocked_count} blocked issues immediately")
            
            progress = standup_data.get("sprint_progress", "0%")
            if progress.replace("%", "").replace(".", "").isdigit():
                progress_num = float(progress.replace("%", ""))
                if progress_num < 50:
                    recommendations.append("⚠️ Sprint progress is below 50% - consider scope adjustment")
        
        if isinstance(burndown_data, dict):
            completion = burndown_data.get("completion_percentage", 0)
            if completion > 80:
                recommendations.append("🎉 Sprint is on track for successful completion")
            elif completion < 30:
                recommendations.append("📈 Consider adding team capacity or reducing scope")
        
        return recommendations


# Global coordinator instance for ADK web interface
scrum_master_coordinator = ScrumMasterCoordinator()
