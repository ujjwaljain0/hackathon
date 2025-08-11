"""Confluence agent that communicates via MCP servers (stubbed)."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from ..core.agent_base import BaseAgent
from ..core.types import Command
from ..integrations.mcp_client import MCPClient
from ..models.confluence import ConfluencePage

logger = logging.getLogger(__name__)


class ConfluenceAgent(BaseAgent):
    def __init__(self, mcp_server_url: str = "http://localhost:8001") -> None:
        self.mcp_client = MCPClient(mcp_server_url, "confluence")
        self.agent_name = "confluence_agent"
        self.cache: Dict[str, Any] = {}
        self.cache_ttl_seconds = 300
        self._last_cleanup: datetime = datetime.now()

    async def initialize(self) -> bool:
        return await self.mcp_client.connect()

    async def execute_command(self, command: Command) -> Any:
        action = command.action
        params = command.parameters
        if action == "get_page":
            return await self.get_page(**params)
        if action == "create_page":
            return await self.create_page(**params)
        if action == "update_page":
            return await self.update_page(**params)
        raise ValueError(f"Unknown Confluence action: {action}")

    async def get_page(
        self,
        page_id: Optional[str] = None,
        title: Optional[str] = None,
        space_key: Optional[str] = None,
    ) -> Optional[ConfluencePage]:
        cache_key = f"page:{page_id}:{title}:{space_key}"
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached

        response = await self.mcp_client.request(
            "/confluence/pages",
            method="GET",
            params={"pageId": page_id or "", "title": title or "", "spaceKey": space_key or ""},
        )
        pages = response.get("pages", [])
        if not pages:
            return None
        data = pages[0]
        page = ConfluencePage(
            id=data["id"],
            title=data["title"],
            content=data["content"],
            space_key=data["spaceKey"],
            parent_id=data.get("parentId"),
            version=data["version"],
            status=data["status"],
            created=datetime.fromisoformat(data["created"]),
            updated=datetime.fromisoformat(data["updated"]),
            author=data["author"],
            labels=data.get("labels", []),
            attachments=data.get("attachments", []),
            children=data.get("children", []),
        )
        self._set_cache(cache_key, page)
        return page

    async def create_page(
        self,
        title: str,
        content: str,
        space_key: str,
        parent_id: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> ConfluencePage:
        payload = {"title": title, "content": content, "spaceKey": space_key, "parentId": parent_id, "labels": labels or []}
        resp = await self.mcp_client.request("/confluence/pages", method="POST", json=payload)
        return ConfluencePage(
            id=resp["id"],
            title=resp["title"],
            content=resp["content"],
            space_key=resp["spaceKey"],
            parent_id=resp.get("parentId"),
            version=resp["version"],
            status=resp["status"],
            created=datetime.fromisoformat(resp["created"]),
            updated=datetime.fromisoformat(resp["updated"]),
            author=resp["author"],
            labels=resp.get("labels", []),
            attachments=resp.get("attachments", []),
            children=resp.get("children", []),
        )

    async def update_page(self, page_id: str, updates: Dict[str, Any]) -> ConfluencePage:
        resp = await self.mcp_client.request(f"/confluence/pages/{page_id}", method="PUT", json=updates)
        return ConfluencePage(
            id=resp["id"],
            title=resp["title"],
            content=resp["content"],
            space_key=resp["spaceKey"],
            parent_id=resp.get("parentId"),
            version=resp["version"],
            status=resp["status"],
            created=datetime.fromisoformat(resp["created"]),
            updated=datetime.fromisoformat(resp["updated"]),
            author=resp["author"],
            labels=resp.get("labels", []),
            attachments=resp.get("attachments", []),
            children=resp.get("children", []),
        )

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

    def _cleanup_cache(self) -> None:
        if (datetime.now() - self._last_cleanup) < timedelta(minutes=5):
            return
        to_delete = [k for k, v in self.cache.items() if (datetime.now() - v["ts"]) > timedelta(seconds=self.cache_ttl_seconds)]
        for k in to_delete:
            self.cache.pop(k, None)
        self._last_cleanup = datetime.now()

    async def shutdown(self) -> None:
        await self.mcp_client.disconnect()
