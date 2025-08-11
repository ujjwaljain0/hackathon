"""Jira data models."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class JiraIssue:
    key: str
    summary: str
    description: Optional[str]
    status: str
    priority: str
    assignee: Optional[str]
    reporter: str
    created: datetime
    updated: datetime
    project: str
    issue_type: str
    labels: List[str]
    components: List[str]
    epic_link: Optional[str] = None
    sprint: Optional[str] = None


@dataclass
class JiraProject:
    key: str
    name: str
    description: Optional[str]
    lead: str
    project_type: str
    category: Optional[str]
    url: str
    components: List[str]
    issue_types: List[str]


@dataclass
class JiraSprint:
    id: int
    name: str
    state: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    goal: Optional[str]
    board_id: int
    rapid_view_id: int
