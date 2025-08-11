"""Shared MCP client for communicating with MCP servers (remote-ready).

Features:
- Remote HTTPS URLs supported out of the box
- Env-driven auth headers (Bearer tokens, API keys)
- Configurable timeouts and simple retry logic
"""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import aiohttp
from aiohttp import ClientTimeout
import ssl

logger = logging.getLogger(__name__)


class MCPClient:
    """Async HTTP client for MCP servers (health + basic requests)."""

    def __init__(
        self,
        base_url: str,
        service: str,
        headers: Optional[Dict[str, str]] = None,
        timeout_seconds: int = 30,
        max_retries: int = 2,
        verify_ssl: bool = True,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.service = service
        self.session: Optional[aiohttp.ClientSession] = None
        self.connected = False
        self.timeout = ClientTimeout(total=timeout_seconds)
        self.max_retries = max_retries
        self.verify_ssl = verify_ssl
        
        # Create SSL context
        if not verify_ssl:
            self.ssl_context = ssl.create_default_context()
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE
        else:
            self.ssl_context = None

        # Compose default headers from environment
        env_headers: Dict[str, str] = {}
        # Prefer service-specific env vars, fallback to generic
        token = os.getenv(f"{service.upper()}_MCP_AUTH_TOKEN") or os.getenv("MCP_AUTH_TOKEN")
        api_key = os.getenv(f"{service.upper()}_MCP_API_KEY") or os.getenv("MCP_API_KEY")
        if token:
            # Support both Bearer and Basic auth formats
            if token.startswith("Basic ") or token.startswith("Bearer "):
                env_headers["Authorization"] = token
            else:
                env_headers["Authorization"] = f"Bearer {token}"
        if api_key:
            env_headers["x-api-key"] = api_key

        self.headers: Dict[str, str] = {**env_headers, **(headers or {})}

    async def connect(self) -> bool:
        try:
            connector = aiohttp.TCPConnector(ssl=self.ssl_context) if not self.verify_ssl else None
            self.session = aiohttp.ClientSession(
                timeout=self.timeout, 
                headers=self.headers or None,
                connector=connector
            )
            # Use different health check endpoints for different services
            if "jira" in self.service.lower():
                health_endpoint = "/serverInfo"
            elif "confluence" in self.service.lower():
                health_endpoint = "/space"
            else:
                health_endpoint = "/health"
                
            async with self.session.get(f"{self.base_url}{health_endpoint}") as resp:
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

        method_upper = method.upper()
        for attempt in range(self.max_retries + 1):
            try:
                if method_upper == "GET":
                    async with self.session.get(url) as resp:
                        return await self._parse_response(url, resp)
                if method_upper == "POST":
                    async with self.session.post(url, json=json) as resp:
                        return await self._parse_response(url, resp)
                if method_upper == "PUT":
                    async with self.session.put(url, json=json) as resp:
                        return await self._parse_response(url, resp)
                if method_upper == "DELETE":
                    async with self.session.delete(url) as resp:
                        return await self._parse_response(url, resp)
                raise ValueError(f"Unsupported method: {method}")
            except Exception as exc:  # noqa: BLE001
                is_last = attempt >= self.max_retries
                logger.warning(
                    "MCP request error (%s %s) attempt %d/%d: %s",
                    method_upper,
                    url,
                    attempt + 1,
                    self.max_retries + 1,
                    exc,
                )
                if is_last:
                    raise

    async def _parse_response(self, url: str, resp: aiohttp.ClientResponse) -> Dict[str, Any]:  # type: ignore[name-defined]
        """Parse response with error handling, returning JSON dict.

        - For non-2xx, attempt to return JSON error body, else raise with status.
        - For non-JSON, wrap as {"text": body}.
        """
        status = resp.status
        content_type = resp.headers.get("Content-Type", "")
        if status >= 400:
            try:
                data = await resp.json()
            except Exception:
                text = await resp.text()
                data = {"error": text}
            logger.error("MCP error %s %s: %s", status, url, data)
            raise aiohttp.ClientResponseError(
                request_info=resp.request_info,
                history=resp.history,
                status=status,
                message=str(data),
                headers=resp.headers,
            )
        if "application/json" in content_type:
            return await resp.json()
        # fallback to text
        text = await resp.text()
        return {"text": text}
