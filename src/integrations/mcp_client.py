"""Shared MCP client for communicating with MCP servers (stubs/REST)."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import aiohttp

logger = logging.getLogger(__name__)


class MCPClient:
    """Minimal async HTTP client for MCP servers (health + basic requests)."""

    def __init__(self, base_url: str, service: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.service = service
        self.session: Optional[aiohttp.ClientSession] = None
        self.connected = False

    async def connect(self) -> bool:
        try:
            self.session = aiohttp.ClientSession()
            async with self.session.get(f"{self.base_url}/health") as resp:
                self.connected = resp.status == 200
                if not self.connected:
                    logger.error("%s MCP health check failed: %s", self.service, resp.status)
                return self.connected
        except Exception as exc:  # noqa: BLE001
            logger.error("%s MCP connect error: %s", self.service, exc)
            return False

    async def disconnect(self) -> None:
        if self.session:
            await self.session.close()
        self.session = None
        self.connected = False

    async def request(
        self,
        endpoint: str,
        method: str = "GET",
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not self.connected or not self.session:
            raise ConnectionError("Not connected to MCP server")

        url = f"{self.base_url}{endpoint}"
        if params:
            url = f"{url}?{urlencode(params)}"

        try:
            method_upper = method.upper()
            if method_upper == "GET":
                async with self.session.get(url) as resp:
                    return await resp.json()
            if method_upper == "POST":
                async with self.session.post(url, json=json) as resp:
                    return await resp.json()
            if method_upper == "PUT":
                async with self.session.put(url, json=json) as resp:
                    return await resp.json()
            if method_upper == "DELETE":
                async with self.session.delete(url) as resp:
                    return await resp.json()
            raise ValueError(f"Unsupported method: {method}")
        except Exception as exc:  # noqa: BLE001
            logger.error("MCP request error %s %s: %s", method, url, exc)
            raise
