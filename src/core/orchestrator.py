"""Core orchestrator that routes commands to registered sub-agents asynchronously."""
from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional

from .types import AgentResponse, Command, CommandType
from .agent_base import BaseAgent

logger = logging.getLogger(__name__)


class Orchestrator:
    """Coordinates commands and routes them to registered agents."""

    def __init__(self, max_concurrent_commands: int = 10) -> None:
        self.agents: Dict[str, BaseAgent] = {}
        self.command_history: List[Command] = []
        self.response_cache: Dict[str, AgentResponse] = {}
        self.max_concurrent_commands = max_concurrent_commands
        self.command_semaphore = asyncio.Semaphore(max_concurrent_commands)

    async def register_agent(self, agent_name: str, agent_instance: BaseAgent) -> None:
        if agent_name in self.agents:
            logger.warning("Agent %s already registered, overwriting", agent_name)
        self.agents[agent_name] = agent_instance
        logger.info("Registered agent: %s", agent_name)

    def _route_command(self, command: Command) -> List[str]:
        target_agents: List[str] = []
        if command.command_type in {CommandType.JIRA_ISSUE, CommandType.JIRA_PROJECT, CommandType.JIRA_SPRINT}:
            if "jira_agent" in self.agents:
                target_agents.append("jira_agent")
        elif command.command_type in {CommandType.CONFLUENCE_PAGE, CommandType.CONFLUENCE_SPACE}:
            if "confluence_agent" in self.agents:
                target_agents.append("confluence_agent")
        elif command.command_type in {CommandType.PROJECT_MANAGEMENT, CommandType.SCRUM_MASTER}:
            for name in ("jira_agent", "confluence_agent"):
                if name in self.agents:
                    target_agents.append(name)
        return target_agents

    async def execute_command(self, command: Command) -> List[AgentResponse]:
        start_time = time.time()
        if command.timestamp is None:
            command.timestamp = start_time
        self.command_history.append(command)

        targets = self._route_command(command)
        if not targets:
            return [AgentResponse("orchestrator", False, None, f"No agents for {command.command_type}")]

        async with self.command_semaphore:
            tasks = [self._execute_agent_command(self.agents[name], name, command) for name in targets]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        responses: List[AgentResponse] = []
        for idx, res in enumerate(results):
            if isinstance(res, Exception):
                logger.exception("Agent %s failed", targets[idx])
                responses.append(AgentResponse(targets[idx], False, None, str(res)))
            else:
                responses.append(res)
                if res.success:
                    self.response_cache[f"{command.command_id}_{res.agent_name}"] = res

        logger.info("Command %s completed in %.2fs", command.command_id, time.time() - start_time)
        return responses

    async def _execute_agent_command(self, agent: BaseAgent, agent_name: str, command: Command) -> AgentResponse:
        start = time.time()
        try:
            result = await agent.execute_command(command)
            return AgentResponse(agent_name, True, result, execution_time=time.time() - start)
        except Exception as exc:  # noqa: BLE001 - propagate as structured error
            return AgentResponse(agent_name, False, None, error_message=str(exc), execution_time=time.time() - start)

    async def get_command_status(self, command_id: str) -> Optional[Dict[str, Any]]:
        cmd = next((c for c in self.command_history if c.command_id == command_id), None)
        if not cmd:
            return None
        responses = {
            name: resp for name, resp in self.response_cache.items() if name.startswith(f"{command_id}_")
        }
        return {
            "command": cmd,
            "responses": responses,
            "total_agents": len(self.agents),
            "responding_agents": len(responses),
        }

    def get_system_status(self) -> Dict[str, Any]:
        return {
            "total_agents": len(self.agents),
            "registered_agents": list(self.agents.keys()),
            "total_commands": len(self.command_history),
            "cached_responses": len(self.response_cache),
            "max_concurrent_commands": self.max_concurrent_commands,
            "available_concurrent_slots": self.command_semaphore._value,  # type: ignore[attr-defined]
        }

    async def shutdown(self) -> None:
        for name, agent in self.agents.items():
            if hasattr(agent, "shutdown"):
                try:
                    await agent.shutdown()
                except Exception:  # noqa: BLE001
                    logger.exception("Failed to shutdown agent %s", name)
        self.response_cache.clear()
        self.command_history.clear()
