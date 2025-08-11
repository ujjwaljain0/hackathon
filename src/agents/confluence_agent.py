"""Confluence agent that communicates via MCP servers (stubbed)."""
from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from ..core.agent_base import BaseAgent
from ..core.types import Command
from ..integrations.mcp_client import MCPClient
from ..models.confluence import ConfluencePage

logger = logging.getLogger(__name__)


class ConfluenceAgent(BaseAgent):
    def __init__(self, mcp_server_url: str = "https://athonprompt.atlassian.net/wiki/rest/api") -> None:
        # Disable SSL verification for development - configure verify_ssl=True for production
        verify_ssl = os.getenv("MCP_VERIFY_SSL", "false").lower() == "true"
        self.mcp_client = MCPClient(mcp_server_url, "confluence", verify_ssl=verify_ssl)
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

        # Use Confluence REST API search
        if page_id:
            response = await self.mcp_client.request(f"/content/{page_id}", method="GET", params={"expand": "body.storage,space,version,ancestors"})
            pages = [response] if response else []
        else:
            params = {"expand": "body.storage,space,version,ancestors"}
            if title:
                params["title"] = title
            if space_key:
                params["spaceKey"] = space_key
            response = await self.mcp_client.request("/content", method="GET", params=params)
            pages = response.get("results", [])
        if not pages:
            return None
        data = pages[0]
        page = ConfluencePage(
            id=data["id"],
            title=data["title"],
            content=data.get("body", {}).get("storage", {}).get("value", ""),
            space_key=data.get("space", {}).get("key", ""),
            parent_id=data.get("ancestors", [])[-1]["id"] if data.get("ancestors") else None,
            version=data.get("version", {}).get("number", 1),
            status=data.get("status", "current"),
            created=datetime.fromisoformat(data.get("createdDate", "").replace("Z", "+00:00")) if data.get("createdDate") else datetime.now(),
            updated=datetime.fromisoformat(data.get("version", {}).get("when", "").replace("Z", "+00:00")) if data.get("version", {}).get("when") else datetime.now(),
            author=data.get("version", {}).get("by", {}).get("displayName", ""),
            labels=data.get("metadata", {}).get("labels", {}).get("results", []),
            attachments=[],
            children=[],
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
        logger.info(f"📄 Creating Confluence page in space '{space_key}': {title}")
        logger.info(f"📝 Page details - Parent ID: {parent_id}, Content length: {len(content)} chars")
        
        payload = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "body": {
                "storage": {
                    "value": content,
                    "representation": "storage"
                }
            }
        }
        
        if parent_id:
            payload["ancestors"] = [{"id": parent_id}]
            
        resp = await self.mcp_client.request("/content", method="POST", json=payload)
        
        page = ConfluencePage(
            id=resp["id"],
            title=resp["title"],
            content=resp.get("body", {}).get("storage", {}).get("value", ""),
            space_key=resp.get("space", {}).get("key", ""),
            parent_id=resp.get("ancestors", [])[-1]["id"] if resp.get("ancestors") else None,
            version=resp.get("version", {}).get("number", 1),
            status=resp.get("status", "current"),
            created=datetime.fromisoformat(resp.get("createdDate", "").replace("Z", "+00:00")) if resp.get("createdDate") else datetime.now(),
            updated=datetime.fromisoformat(resp.get("version", {}).get("when", "").replace("Z", "+00:00")) if resp.get("version", {}).get("when") else datetime.now(),
            author=resp.get("version", {}).get("by", {}).get("displayName", ""),
            labels=resp.get("metadata", {}).get("labels", {}).get("results", []),
            attachments=[],
            children=[],
        )
        
        # Log detailed creation information
        logger.info(f"🎯 Confluence Page Created Successfully:")
        logger.info(f"   📌 ID: {page.id}")
        logger.info(f"   📋 Title: {page.title}")
        logger.info(f"   🏗️ Space: {page.space_key}")
        logger.info(f"   📄 Version: {page.version}")
        logger.info(f"   📅 Created: {page.created.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"   👤 Author: {page.author or 'Unknown'}")
        logger.info(f"   🔗 URL: https://athonprompt.atlassian.net/wiki/spaces/{page.space_key}/pages/{page.id}")
        
        return page

    async def update_page(self, page_id: str, updates: Dict[str, Any]) -> ConfluencePage:
        logger.info(f"🔄 Updating Confluence page: {page_id}")
        logger.info(f"📝 Updates: {updates}")
        
        # Get current page version first
        current_page = await self.mcp_client.request(f"/content/{page_id}", params={"expand": "version"})
        current_version = current_page.get("version", {}).get("number", 1)
        
        payload = {
            "version": {"number": current_version + 1},
            **updates
        }
        
        resp = await self.mcp_client.request(f"/content/{page_id}", method="PUT", json=payload)
        
        page = ConfluencePage(
            id=resp["id"],
            title=resp["title"],
            content=resp.get("body", {}).get("storage", {}).get("value", ""),
            space_key=resp.get("space", {}).get("key", ""),
            parent_id=resp.get("ancestors", [])[-1]["id"] if resp.get("ancestors") else None,
            version=resp.get("version", {}).get("number", 1),
            status=resp.get("status", "current"),
            created=datetime.fromisoformat(resp.get("createdDate", "").replace("Z", "+00:00")) if resp.get("createdDate") else datetime.now(),
            updated=datetime.fromisoformat(resp.get("version", {}).get("when", "").replace("Z", "+00:00")) if resp.get("version", {}).get("when") else datetime.now(),
            author=resp.get("version", {}).get("by", {}).get("displayName", ""),
            labels=resp.get("metadata", {}).get("labels", {}).get("results", []),
            attachments=[],
            children=[],
        )
        
        # Log detailed update information  
        logger.info(f"🎯 Confluence Page Updated Successfully:")
        logger.info(f"   📌 ID: {page.id}")
        logger.info(f"   📋 Title: {page.title}")
        logger.info(f"   🏗️ Space: {page.space_key}")
        logger.info(f"   📄 Version: {page.version}")
        logger.info(f"   📅 Updated: {page.updated.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"   👤 Author: {page.author or 'Unknown'}")
        logger.info(f"   🔗 URL: https://athonprompt.atlassian.net/wiki/spaces/{page.space_key}/pages/{page.id}")
        
        return page

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
