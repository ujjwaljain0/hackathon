"""Pydantic models for AI Scrum Master REST API."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Priority(str, Enum):
    """Issue priority levels."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class IssueType(str, Enum):
    """Jira issue types."""
    TASK = "Task"
    BUG = "Bug"
    STORY = "Story"
    EPIC = "Epic"
    INCIDENT = "[System] Incident"
    SERVICE_REQUEST = "[System] Service request"


class TeamMember(BaseModel):
    """Team member information."""
    username: str = Field(..., description="Jira username")
    display_name: str = Field(..., description="Display name")
    email: Optional[str] = Field(None, description="Email address")
    skills: List[str] = Field(default_factory=list, description="Technical skills")
    capacity: float = Field(default=1.0, description="Work capacity (0.0-1.0)")


class ProjectRequirement(BaseModel):
    """Single project requirement/feature."""
    title: str = Field(..., description="Requirement title")
    description: str = Field(..., description="Detailed description")
    priority: Priority = Field(default=Priority.MEDIUM, description="Priority level")
    estimated_hours: Optional[int] = Field(None, description="Estimated work hours")
    required_skills: List[str] = Field(default_factory=list, description="Required technical skills")
    dependencies: List[str] = Field(default_factory=list, description="Dependencies on other requirements")


class ProjectRequest(BaseModel):
    """Complete project request with requirements and team."""
    project_name: str = Field(..., description="Project name")
    project_description: str = Field(..., description="High-level project description")
    jira_project_key: str = Field(..., description="Jira project key (e.g., 'SUP')")
    confluence_space_key: str = Field(..., description="Confluence space key (e.g., 'MFS')")
    
    requirements: List[ProjectRequirement] = Field(..., description="List of project requirements")
    team_members: List[TeamMember] = Field(..., description="Available team members")
    
    deadline: Optional[datetime] = Field(None, description="Project deadline")
    auto_assign: bool = Field(default=True, description="Automatically assign tasks to team members")
    create_confluence_docs: bool = Field(default=True, description="Create Confluence documentation")


class GeneratedJiraIssue(BaseModel):
    """Generated Jira issue information."""
    key: str = Field(..., description="Jira issue key")
    title: str = Field(..., description="Issue title")
    description: str = Field(..., description="Issue description")
    assignee: Optional[str] = Field(None, description="Assigned team member")
    priority: str = Field(..., description="Issue priority")
    issue_type: str = Field(..., description="Issue type")
    estimated_hours: Optional[int] = Field(None, description="Estimated hours")
    url: str = Field(..., description="Direct URL to Jira issue")


class GeneratedConfluencePage(BaseModel):
    """Generated Confluence page information."""
    id: str = Field(..., description="Confluence page ID")
    title: str = Field(..., description="Page title")
    space_key: str = Field(..., description="Space key")
    url: str = Field(..., description="Direct URL to Confluence page")


class ProjectExecutionResult(BaseModel):
    """Result of project execution."""
    project_name: str = Field(..., description="Project name")
    execution_id: str = Field(..., description="Unique execution ID")
    status: str = Field(..., description="Execution status")
    
    jira_issues: List[GeneratedJiraIssue] = Field(default_factory=list, description="Created Jira issues")
    confluence_pages: List[GeneratedConfluencePage] = Field(default_factory=list, description="Created Confluence pages")
    
    team_assignments: Dict[str, List[str]] = Field(default_factory=dict, description="Team member to issue keys mapping")
    estimated_total_hours: int = Field(default=0, description="Total estimated project hours")
    
    errors: List[str] = Field(default_factory=list, description="Any errors during execution")
    warnings: List[str] = Field(default_factory=list, description="Any warnings during execution")
    
    created_at: datetime = Field(default_factory=datetime.now, description="Execution timestamp")


class HealthCheck(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now, description="Check timestamp")
    services: Dict[str, bool] = Field(..., description="Individual service statuses")
    version: str = Field(default="1.0.0", description="API version")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")


# API Response models
class ProjectExecutionResponse(BaseModel):
    """Response for project execution endpoint."""
    success: bool = Field(..., description="Whether execution was successful")
    message: str = Field(..., description="Human-readable message")
    data: Optional[ProjectExecutionResult] = Field(None, description="Execution results")
    error: Optional[str] = Field(None, description="Error message if failed")


class TeamMemberSuggestion(BaseModel):
    """Suggested team member assignment."""
    username: str = Field(..., description="Team member username")
    display_name: str = Field(..., description="Team member display name")
    match_score: float = Field(..., description="Skill match score (0.0-1.0)")
    matching_skills: List[str] = Field(..., description="Skills that match the requirement")
    current_workload: float = Field(..., description="Current workload percentage")


class RequirementBreakdown(BaseModel):
    """Breakdown of a requirement into tasks."""
    original_requirement: str = Field(..., description="Original requirement title")
    suggested_tasks: List[Dict[str, Any]] = Field(..., description="Suggested task breakdown")
    suggested_assignees: List[TeamMemberSuggestion] = Field(..., description="Suggested team member assignments")
    estimated_total_hours: int = Field(..., description="Total estimated hours for this requirement")


class SprintCreationRequest(BaseModel):
    """Request to create a new sprint with AI assistance."""
    sprint_name: str = Field(..., description="Name of the sprint")
    sprint_goal: str = Field(..., description="Sprint goal/objective")
    duration_weeks: int = Field(default=2, description="Sprint duration in weeks")
    
    # Project context
    jira_project_key: str = Field(..., description="Jira project key (e.g., 'SUP')")
    confluence_space_key: Optional[str] = Field(None, description="Confluence space key for documentation")
    
    # Sprint requirements and context
    requirements: str = Field(..., description="All relevant information about what needs to be done in this sprint")
    
    # Team information
    team_members: List[TeamMember] = Field(default_factory=list, description="Available team members")
    team_capacity: float = Field(default=1.0, description="Team capacity for this sprint (0.0-1.0)")
    
    # Optional settings
    auto_assign_tasks: bool = Field(default=True, description="Automatically assign tasks to team members")
    create_documentation: bool = Field(default=True, description="Create sprint planning documentation")


class SprintCreationResult(BaseModel):
    """Result of sprint creation."""
    sprint_name: str = Field(..., description="Created sprint name")
    sprint_id: Optional[str] = Field(None, description="Jira sprint ID if created")
    sprint_url: Optional[str] = Field(None, description="Direct URL to sprint")
    
    # Created artifacts
    jira_issues: List[GeneratedJiraIssue] = Field(default_factory=list, description="Created Jira issues")
    confluence_pages: List[GeneratedConfluencePage] = Field(default_factory=list, description="Created documentation pages")
    
    # Sprint planning details
    total_story_points: int = Field(default=0, description="Total story points planned")
    estimated_hours: int = Field(default=0, description="Total estimated hours")
    team_assignments: Dict[str, List[str]] = Field(default_factory=dict, description="Team member assignments")
    
    # AI insights
    scrum_master_notes: List[str] = Field(default_factory=list, description="AI Scrum Master insights and recommendations")
    capacity_analysis: str = Field(default="", description="Team capacity analysis")
    
    # Status
    status: str = Field(..., description="Creation status")
    errors: List[str] = Field(default_factory=list, description="Any errors during creation")
    warnings: List[str] = Field(default_factory=list, description="Any warnings during creation")
    
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")


class SprintCreationResponse(BaseModel):
    """Response for sprint creation endpoint."""
    success: bool = Field(..., description="Whether sprint creation was successful")
    message: str = Field(..., description="Human-readable message")
    data: Optional[SprintCreationResult] = Field(None, description="Sprint creation results")
    error: Optional[str] = Field(None, description="Error message if failed")
