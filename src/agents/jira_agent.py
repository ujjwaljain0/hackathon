"""Jira agent that communicates via MCP servers (stubbed)."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from ..core.agent_base import BaseAgent
from ..core.types import Command
from ..integrations.mcp_client import MCPClient
from ..models.jira import JiraIssue

logger = logging.getLogger(__name__)


class JiraAgent(BaseAgent):
    def __init__(self, mcp_server_url: str = "http://localhost:8000") -> None:
        self.mcp_client = MCPClient(mcp_server_url, "jira")
        self.agent_name = "jira_agent"
        self.cache: Dict[str, Any] = {}
        self.cache_ttl_seconds = 300
        self._last_cleanup: datetime = datetime.now()

    async def initialize(self) -> bool:
        return await self.mcp_client.connect()

    async def execute_command(self, command: Command) -> Any:
        action = command.action
        params = command.parameters
        if action == "get_issues":
            return await self.get_issues(**params)
        if action == "create_issue":
            return await self.create_issue(**params)
        if action == "update_issue":
            return await self.update_issue(**params)
        raise ValueError(f"Unknown Jira action: {action}")

    async def get_issues(
        self,
        project: Optional[str] = None,
        status: Optional[str] = None,
        assignee: Optional[str] = None,
        issue_type: Optional[str] = None,
        max_results: int = 50,
    ) -> List[JiraIssue]:
        cache_key = f"issues:{project}:{status}:{assignee}:{issue_type}:{max_results}"
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached

        response = await self.mcp_client.request(
            "/jira/issues", method="GET", params={
                "project": project or "",
                "status": status or "",
                "assignee": assignee or "",
                "issueType": issue_type or "",
                "maxResults": max_results,
            }
        )
        issues: List[JiraIssue] = []
        for data in response.get("issues", []):
            issues.append(
                JiraIssue(
                    key=data["key"],
                    summary=data["summary"],
                    description=data.get("description"),
                    status=data["status"],
                    priority=data["priority"],
                    assignee=data.get("assignee"),
                    reporter=data["reporter"],
                    created=datetime.fromisoformat(data["created"]),
                    updated=datetime.fromisoformat(data["updated"]),
                    project=data["project"],
                    issue_type=data["issueType"],
                    labels=data.get("labels", []),
                    components=data.get("components", []),
                    epic_link=data.get("epicLink"),
                    sprint=data.get("sprint"),
                )
            )
        self._set_cache(cache_key, issues)
        return issues

    async def create_issue(
        self,
        project: str,
        summary: str,
        description: Optional[str] = None,
        issue_type: str = "Task",
        priority: str = "Medium",
        assignee: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> JiraIssue:
        payload = {
            "project": project,
            "summary": summary,
            "description": description or "",
            "issueType": issue_type,
            "priority": priority,
            "assignee": assignee,
            "labels": labels or [],
        }
        resp = await self.mcp_client.request("/jira/issues", method="POST", json=payload)
        issue = JiraIssue(
            key=resp["key"],
            summary=resp["summary"],
            description=resp.get("description"),
            status=resp["status"],
            priority=resp["priority"],
            assignee=resp.get("assignee"),
            reporter=resp["reporter"],
            created=datetime.fromisoformat(resp["created"]),
            updated=datetime.fromisoformat(resp["updated"]),
            project=resp["project"],
            issue_type=resp["issueType"],
            labels=resp.get("labels", []),
            components=resp.get("components", []),
            epic_link=resp.get("epicLink"),
            sprint=resp.get("sprint"),
        )
        self._invalidate_project_cache(project)
        return issue

    async def update_issue(self, issue_key: str, updates: Dict[str, Any]) -> JiraIssue:
        resp = await self.mcp_client.request(f"/jira/issues/{issue_key}", method="PUT", json=updates)
        issue = JiraIssue(
            key=resp["key"],
            summary=resp["summary"],
            description=resp.get("description"),
            status=resp["status"],
            priority=resp["priority"],
            assignee=resp.get("assignee"),
            reporter=resp["reporter"],
            created=datetime.fromisoformat(resp["created"]),
            updated=datetime.fromisoformat(resp["updated"]),
            project=resp["project"],
            issue_type=resp["issueType"],
            labels=resp.get("labels", []),
            components=resp.get("components", []),
            epic_link=resp.get("epicLink"),
            sprint=resp.get("sprint"),
        )
        self._invalidate_project_cache(issue.project)
        return issue

    def _get_cache(self, key: str):
        self._cleanup_cache()
        entry = self.cache.get(key)
        if not entry:
            return None
        if (datetime.now() - entry["ts"]) > timedelta(seconds=self.cache_ttl_seconds):
            self.cache.pop(key, None)
            return None
        return entry["val"]

    def _set_cache(self, key: str, value: Any) -> None:
        self.cache[key] = {"val": value, "ts": datetime.now()}

    def _invalidate_project_cache(self, project: str) -> None:
        to_delete = [k for k in self.cache.keys() if f":{project}:" in k]
        for k in to_delete:
            self.cache.pop(k, None)

    def _cleanup_cache(self) -> None:
        if (datetime.now() - self._last_cleanup) < timedelta(minutes=5):
            return
        to_delete = [k for k, v in self.cache.items() if (datetime.now() - v["ts"]) > timedelta(seconds=self.cache_ttl_seconds)]
        for k in to_delete:
            self.cache.pop(k, None)
        self._last_cleanup = datetime.now()

    async def shutdown(self) -> None:
        await self.mcp_client.disconnect()
