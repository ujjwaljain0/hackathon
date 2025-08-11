"""Base agent protocol defining the agent interface."""
from __future__ import annotations

from typing import Any, Protocol
from .types import Command


class BaseAgent(Protocol):
    agent_name: str

    async def initialize(self) -> bool:  # pragma: no cover - stub
        """Initialize the agent (e.g., connect to MCP)."""
        ...

    async def execute_command(self, command: Command) -> Any:  # pragma: no cover - stub
        """Execute a command and return the result."""
        ...

    async def shutdown(self) -> None:  # pragma: no cover - stub
        """Gracefully shutdown the agent."""
        ...
