"""Jira agent that communicates via MCP servers (stubbed)."""
from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from ..core.agent_base import BaseAgent
from ..core.types import Command
from ..integrations.mcp_client import MCPClient
from ..models.jira import JiraIssue

logger = logging.getLogger(__name__)


class JiraAgent(BaseAgent):
    def __init__(self, mcp_server_url: str = "https://athonprompt.atlassian.net/rest/api/3") -> None:
        # Disable SSL verification for development - configure verify_ssl=True for production
        verify_ssl = os.getenv("MCP_VERIFY_SSL", "false").lower() == "true"
        self.mcp_client = MCPClient(mcp_server_url, "jira", verify_ssl=verify_ssl)
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

    async def get_projects(self) -> List[Dict[str, Any]]:
        """Get list of available projects from Jira."""
        cache_key = "projects:list"
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached

        try:
            response = await self.mcp_client.request("/project", method="GET")
            projects = response if isinstance(response, list) else []
            self._set_cache(cache_key, projects)
            logger.info(f"📋 Retrieved {len(projects)} available Jira projects")
            return projects
        except Exception as e:
            logger.error(f"❌ Failed to retrieve projects: {str(e)}")
            return []

    async def find_project_by_name(self, project_name: str) -> Optional[str]:
        """Find project key by project name (case-insensitive search)."""
        projects = await self.get_projects()
        
        # Try exact match first
        for project in projects:
            if project.get("name", "").lower() == project_name.lower():
                return project.get("key", "")
        
        # Try partial match
        for project in projects:
            if project_name.lower() in project.get("name", "").lower():
                return project.get("key", "")
        
        # Try transformed key match
        transformed_key = project_name.replace(" ", "").upper()
        for project in projects:
            if project.get("key", "").upper() == transformed_key:
                return project.get("key", "")
        
        logger.warning(f"⚠️ No project found matching '{project_name}' or transformed key '{transformed_key}'")
        return None

    async def get_issues(
        self,
        project: Optional[str] = None,
        status: Optional[str] = None,
        assignee: Optional[str] = None,
        issue_type: Optional[str] = None,
        max_results: int = 50,
    ) -> List[JiraIssue]:
        # Find the actual project key if project name is provided
        project_key = None
        if project:
            project_key = await self.find_project_by_name(project)
            if not project_key:
                logger.error(f"❌ Project '{project}' not found in Jira")
                return []
        
        cache_key = f"issues:{project_key}:{status}:{assignee}:{issue_type}:{max_results}"
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached

        # Build JQL query for Jira REST API
        jql_parts = []
        if project_key:
            jql_parts.append(f"project = {project_key}")
        if status:
            jql_parts.append(f"status = '{status}'")
        if assignee:
            jql_parts.append(f"assignee = '{assignee}'")
        if issue_type:
            jql_parts.append(f"issuetype = '{issue_type}'")
        
        jql = " AND ".join(jql_parts) if jql_parts else ""
        
        response = await self.mcp_client.request(
            "/search", method="GET", params={
                "jql": jql,
                "maxResults": max_results,
                "fields": "summary,description,status,priority,assignee,reporter,created,updated,project,issuetype,labels,components"
            }
        )
        issues: List[JiraIssue] = []
        for data in response.get("issues", []):
            fields = data.get("fields", {})
            issues.append(
                JiraIssue(
                    key=data["key"],
                    summary=fields.get("summary", ""),
                    description=fields.get("description"),
                    status=fields.get("status", {}).get("name", ""),
                    priority=fields.get("priority", {}).get("name", ""),
                    assignee=fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
                    reporter=fields.get("reporter", {}).get("displayName", ""),
                    created=datetime.fromisoformat(fields.get("created", "").replace("Z", "+00:00")) if fields.get("created") else datetime.now(),
                    updated=datetime.fromisoformat(fields.get("updated", "").replace("Z", "+00:00")) if fields.get("updated") else datetime.now(),
                    project=fields.get("project", {}).get("key", ""),
                    issue_type=fields.get("issuetype", {}).get("name", ""),
                    labels=fields.get("labels", []),
                    components=[c.get("name", "") for c in fields.get("components", [])],
                    epic_link=fields.get("customfield_10014"),  # Epic Link field
                    sprint=fields.get("customfield_10020"),     # Sprint field
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
        # Find the actual project key by project name
        project_key = await self.find_project_by_name(project)
        if not project_key:
            raise ValueError(f"❌ Project '{project}' not found in Jira. Available projects: {[p.get('key', '') for p in await self.get_projects()]}")
        
        logger.info(f"🎫 Creating Jira issue in project '{project}' (key: {project_key}): {summary}")
        logger.info(f"📝 Issue details - Type: {issue_type}, Priority: {priority}, Assignee: {assignee}")
        
        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": description or "",
                "issuetype": {"name": issue_type},
                "priority": {"name": priority},
            }
        }
        
        if assignee:
            payload["fields"]["assignee"] = {"name": assignee}
        if labels:
            payload["fields"]["labels"] = [{"name": label} for label in labels]
            
        resp = await self.mcp_client.request("/issue", method="POST", json=payload)
        # Get the created issue details
        issue_key = resp["key"]
        logger.info(f"✅ Successfully created Jira issue: {issue_key}")
        
        issue_detail = await self.mcp_client.request(f"/issue/{issue_key}")
        
        fields = issue_detail.get("fields", {})
        issue = JiraIssue(
            key=issue_detail["key"],
            summary=fields.get("summary", ""),
            description=fields.get("description"),
            status=fields.get("status", {}).get("name", ""),
            priority=fields.get("priority", {}).get("name", ""),
            assignee=fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
            reporter=fields.get("reporter", {}).get("displayName", ""),
            created=datetime.fromisoformat(fields.get("created", "").replace("Z", "+00:00")) if fields.get("created") else datetime.now(),
            updated=datetime.fromisoformat(fields.get("updated", "").replace("Z", "+00:00")) if fields.get("updated") else datetime.now(),
            project=fields.get("project", {}).get("key", ""),
            issue_type=fields.get("issuetype", {}).get("name", ""),
            labels=fields.get("labels", []),
            components=[c.get("name", "") for c in fields.get("components", [])],
            epic_link=fields.get("customfield_10014"),
            sprint=fields.get("customfield_10020"),
        )
        
        # Log detailed creation information
        logger.info(f"🎯 Jira Issue Created Successfully:")
        logger.info(f"   📌 Key: {issue.key}")
        logger.info(f"   📋 Summary: {issue.summary}")
        logger.info(f"   🏗️ Project: {issue.project}")
        logger.info(f"   🔧 Type: {issue.issue_type}")
        logger.info(f"   ⚡ Priority: {issue.priority}")
        logger.info(f"   👤 Assignee: {issue.assignee or 'Unassigned'}")
        logger.info(f"   📅 Created: {issue.created.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"   🔗 URL: https://athonprompt.atlassian.net/browse/{issue.key}")
        
        # Invalidate cache for the project of the created issue
        if project_key:
            self._invalidate_project_cache(project_key)
        return issue

    async def update_issue(self, issue_key: str, updates: Dict[str, Any]) -> JiraIssue:
        logger.info(f"🔄 Updating Jira issue: {issue_key}")
        logger.info(f"📝 Updates: {updates}")
        
        # Convert updates to Jira REST API format
        payload = {"fields": updates}
        await self.mcp_client.request(f"/issue/{issue_key}", method="PUT", json=payload)
        
        # Get updated issue details
        resp = await self.mcp_client.request(f"/issue/{issue_key}")
        fields = resp.get("fields", {})
        issue = JiraIssue(
            key=resp["key"],
            summary=fields.get("summary", ""),
            description=fields.get("description"),
            status=fields.get("status", {}).get("name", ""),
            priority=fields.get("priority", {}).get("name", ""),
            assignee=fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
            reporter=fields.get("reporter", {}).get("displayName", ""),
            created=datetime.fromisoformat(fields.get("created", "").replace("Z", "+00:00")) if fields.get("created") else datetime.now(),
            updated=datetime.fromisoformat(fields.get("updated", "").replace("Z", "+00:00")) if fields.get("updated") else datetime.now(),
            project=fields.get("project", {}).get("key", ""),
            issue_type=fields.get("issuetype", {}).get("name", ""),
            labels=fields.get("labels", []),
            components=[c.get("name", "") for c in fields.get("components", [])],
            epic_link=fields.get("customfield_10014"),
            sprint=fields.get("customfield_10020"),
        )
        
        # Log detailed update information
        logger.info(f"🎯 Jira Issue Updated Successfully:")
        logger.info(f"   📌 Key: {issue.key}")
        logger.info(f"   📋 Summary: {issue.summary}")
        logger.info(f"   🔧 Type: {issue.issue_type}")
        logger.info(f"   ⚡ Priority: {issue.priority}")
        logger.info(f"   👤 Assignee: {issue.assignee or 'Unassigned'}")
        logger.info(f"   📅 Updated: {issue.updated.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"   🔗 URL: https://athonprompt.atlassian.net/browse/{issue.key}")
        
        # Invalidate cache for the project of the updated issue
        if issue.project:
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
        # Transform project name to valid Jira project key for cache invalidation
        project_key = project.replace(" ", "").upper() if project else ""
        to_delete = [k for k in self.cache.keys() if f":{project_key}:" in k]
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
