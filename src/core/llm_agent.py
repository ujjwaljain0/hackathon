"""Lightweight LLM agent wrappers to match the requested initialization style.

Usage:

LlmAgent(
    name="splunk_query_agent",
    model=LiteLlm(
        model="gpt-4.1-mini",
        api_base="https://api.ai.public.rakuten-it.com/openai/v1",
        api_key=os.getenv("LITELLM_API_KEY"),
    ),
)
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from litellm import completion


@dataclass
class LiteLlm:
    model: str
    api_base: Optional[str] = None
    api_key: Optional[str] = None

    def complete(self, messages: List[Dict[str, str]], tools: Optional[List[Dict[str, Any]]] = None, tool_choice: str = "auto"):
        params: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
        }
        if tools is not None:
            params["tools"] = tools
            params["tool_choice"] = tool_choice
        if self.api_base:
            params["api_base"] = self.api_base
        # Allow LITELLM_API_KEY or OPENAI_API_KEY env fallback
        key = self.api_key or os.getenv("LITELLM_API_KEY") or os.getenv("OPENAI_API_KEY")
        if key:
            params["api_key"] = key
        return completion(**params)


class LlmAgent:
    def __init__(self, name: str, model: LiteLlm, system_prompt: Optional[str] = None) -> None:
        self.name = name
        self.model = model
        self.system_prompt = system_prompt or "You are a helpful orchestration agent. Prefer calling tools."

    def chat(self, user_message: str, tools: Optional[List[Dict[str, Any]]] = None):
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message},
        ]
        return self.model.complete(messages=messages, tools=tools, tool_choice="auto")


