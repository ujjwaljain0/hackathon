"""Core types and data structures for the AI Scrum Master system."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class CommandType(Enum):
    JIRA_ISSUE = "jira_issue"
    JIRA_PROJECT = "jira_project"
    JIRA_SPRINT = "jira_sprint"
    CONFLUENCE_PAGE = "confluence_page"
    CONFLUENCE_SPACE = "confluence_space"
    PROJECT_MANAGEMENT = "project_management"
    SCRUM_MASTER = "scrum_master"
    UNKNOWN = "unknown"


@dataclass
class Command:
    command_id: str
    command_type: CommandType
    action: str
    parameters: Dict[str, Any]
    priority: int = 1
    timestamp: Optional[float] = None


@dataclass
class AgentResponse:
    agent_name: str
    success: bool
    data: Any
    error_message: Optional[str] = None
    execution_time: float = 0.0
