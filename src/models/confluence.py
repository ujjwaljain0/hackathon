"""Confluence data models."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class ConfluencePage:
    id: str
    title: str
    content: str
    space_key: str
    parent_id: Optional[str]
    version: int
    status: str
    created: datetime
    updated: datetime
    author: str
    labels: List[str]
    attachments: List[str]
    children: List[str]


@dataclass
class ConfluenceSpace:
    key: str
    name: str
    description: Optional[str]
    type: str
    status: str
    created: datetime
    updated: datetime
    owner: str
    home_page_id: Optional[str]
    total_pages: int


@dataclass
class ConfluenceAttachment:
    id: str
    filename: str
    content_type: str
    size: int
    page_id: str
    created: datetime
    updated: datetime
    author: str
    comment: Optional[str]
