"""Project orchestrator for breaking down requirements and creating Jira/Confluence content."""
from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from ..core.google_agent_development_kit_coordinator import GoogleAgentDevelopmentKitCoordinator
from .models import (
    GeneratedConfluencePage,
    GeneratedJiraIssue,
    ProjectExecutionResult,
    ProjectRequest,
    ProjectRequirement,
    RequirementBreakdown,
    TeamMember,
    TeamMemberSuggestion,
)

logger = logging.getLogger(__name__)


class ProjectOrchestrator:
    """Orchestrates project breakdown and execution using AI agents."""

    def __init__(self):
        self.coordinator = GoogleAgentDevelopmentKitCoordinator()
        self.execution_history: Dict[str, ProjectExecutionResult] = {}

    async def initialize(self) -> bool:
        """Initialize the coordinator and agents."""
        return await self.coordinator.initialize()

    async def shutdown(self) -> None:
        """Shutdown the coordinator."""
        await self.coordinator.shutdown()

    async def execute_project(self, project_request: ProjectRequest) -> ProjectExecutionResult:
        """Execute a complete project request."""
        execution_id = str(uuid.uuid4())
        logger.info(f"🚀 Starting project execution: {project_request.project_name} (ID: {execution_id})")

        result = ProjectExecutionResult(
            project_name=project_request.project_name,
            execution_id=execution_id,
            status="in_progress",
        )

        try:
            # Step 1: Break down requirements using AI
            logger.info("🧠 Breaking down project requirements with AI...")
            breakdowns = await self._break_down_requirements(project_request)

            # Step 2: Create Confluence documentation if requested
            if project_request.create_confluence_docs:
                logger.info("📄 Creating Confluence documentation...")
                confluence_pages = await self._create_confluence_documentation(
                    project_request, breakdowns
                )
                result.confluence_pages = confluence_pages

            # Step 3: Create Jira issues
            logger.info("🎫 Creating Jira issues...")
            jira_issues, team_assignments = await self._create_jira_issues(
                project_request, breakdowns
            )
            result.jira_issues = jira_issues
            result.team_assignments = team_assignments

            # Step 4: Calculate totals
            result.estimated_total_hours = sum(
                issue.estimated_hours or 0 for issue in jira_issues
            )

            result.status = "completed"
            logger.info(f"✅ Project execution completed: {execution_id}")

        except Exception as e:
            logger.error(f"❌ Project execution failed: {str(e)}")
            result.status = "failed"
            result.errors.append(str(e))

        # Store execution history
        self.execution_history[execution_id] = result
        return result

    async def _break_down_requirements(
        self, project_request: ProjectRequest
    ) -> List[RequirementBreakdown]:
        """Use AI to break down high-level requirements into specific tasks."""
        breakdowns = []

        for requirement in project_request.requirements:
            logger.info(f"🔍 Analyzing requirement: {requirement.title}")

            # Use AI to break down the requirement
            prompt = self._build_breakdown_prompt(requirement, project_request)
            responses = await self.coordinator.chat_execute(prompt)

            # For now, create a simple breakdown
            # In a real implementation, this would parse AI response
            breakdown = RequirementBreakdown(
                original_requirement=requirement.title,
                suggested_tasks=[
                    {
                        "title": f"Implement {requirement.title}",
                        "description": requirement.description,
                        "priority": requirement.priority.value,
                        "estimated_hours": requirement.estimated_hours or 8,
                    }
                ],
                suggested_assignees=self._suggest_assignees(
                    requirement, project_request.team_members
                ),
                estimated_total_hours=requirement.estimated_hours or 8,
            )
            breakdowns.append(breakdown)

        return breakdowns

    async def _create_confluence_documentation(
        self, project_request: ProjectRequest, breakdowns: List[RequirementBreakdown]
    ) -> List[GeneratedConfluencePage]:
        """Create Confluence documentation for the project."""
        pages = []

        # Create main project overview page
        overview_content = self._build_project_overview_content(project_request, breakdowns)
        
        responses = await self.coordinator.chat_execute(
            f"Create a Confluence page in space '{project_request.confluence_space_key}' "
            f"titled '{project_request.project_name} - Project Overview' "
            f"with content: {overview_content}"
        )

        for response in responses:
            if response.success and hasattr(response.data, 'id'):
                page = GeneratedConfluencePage(
                    id=response.data.id,
                    title=response.data.title,
                    space_key=response.data.space_key,
                    url=f"https://athonprompt.atlassian.net/wiki/spaces/{response.data.space_key}/pages/{response.data.id}"
                )
                pages.append(page)

        # Create technical requirements page
        tech_content = self._build_technical_requirements_content(breakdowns)
        
        responses = await self.coordinator.chat_execute(
            f"Create a Confluence page in space '{project_request.confluence_space_key}' "
            f"titled '{project_request.project_name} - Technical Requirements' "
            f"with content: {tech_content}"
        )

        for response in responses:
            if response.success and hasattr(response.data, 'id'):
                page = GeneratedConfluencePage(
                    id=response.data.id,
                    title=response.data.title,
                    space_key=response.data.space_key,
                    url=f"https://athonprompt.atlassian.net/wiki/spaces/{response.data.space_key}/pages/{response.data.id}"
                )
                pages.append(page)

        return pages

    async def _create_jira_issues(
        self, project_request: ProjectRequest, breakdowns: List[RequirementBreakdown]
    ) -> Tuple[List[GeneratedJiraIssue], Dict[str, List[str]]]:
        """Create Jira issues based on requirement breakdowns."""
        issues = []
        team_assignments: Dict[str, List[str]] = {}

        for breakdown in breakdowns:
            for task in breakdown.suggested_tasks:
                # Determine assignee
                assignee = None
                if project_request.auto_assign and breakdown.suggested_assignees:
                    assignee = breakdown.suggested_assignees[0].username

                # Create Jira issue
                responses = await self.coordinator.chat_execute(
                    f"Create a Jira issue in project '{project_request.jira_project_key}' "
                    f"with summary '{task['title']}' "
                    f"and description '{task['description']}' "
                    f"Set priority to '{task['priority']}' and issue type to 'Task'"
                    + (f" and assign to '{assignee}'" if assignee else "")
                )

                for response in responses:
                    if response.success and hasattr(response.data, 'key'):
                        issue = GeneratedJiraIssue(
                            key=response.data.key,
                            title=response.data.summary,
                            description=response.data.description or "",
                            assignee=response.data.assignee,
                            priority=response.data.priority,
                            issue_type=response.data.issue_type,
                            estimated_hours=task.get('estimated_hours'),
                            url=f"https://athonprompt.atlassian.net/browse/{response.data.key}"
                        )
                        issues.append(issue)

                        # Track team assignments
                        if assignee:
                            if assignee not in team_assignments:
                                team_assignments[assignee] = []
                            team_assignments[assignee].append(response.data.key)

        return issues, team_assignments

    def _build_breakdown_prompt(
        self, requirement: ProjectRequirement, project_request: ProjectRequest
    ) -> str:
        """Build a prompt for AI to break down requirements."""
        return (
            f"Break down this project requirement into specific implementable tasks:\n\n"
            f"Project: {project_request.project_name}\n"
            f"Requirement: {requirement.title}\n"
            f"Description: {requirement.description}\n"
            f"Priority: {requirement.priority.value}\n"
            f"Required Skills: {', '.join(requirement.required_skills)}\n\n"
            f"Please suggest 2-4 specific tasks that would implement this requirement, "
            f"considering the technical skills needed and estimated effort."
        )

    def _suggest_assignees(
        self, requirement: ProjectRequirement, team_members: List[TeamMember]
    ) -> List[TeamMemberSuggestion]:
        """Suggest team members for a requirement based on skills and capacity."""
        suggestions = []

        for member in team_members:
            # Calculate skill match score
            if requirement.required_skills:
                matching_skills = [
                    skill for skill in requirement.required_skills 
                    if skill.lower() in [s.lower() for s in member.skills]
                ]
                match_score = len(matching_skills) / len(requirement.required_skills)
            else:
                matching_skills = []
                match_score = 0.5  # Default score when no specific skills required

            # Factor in capacity
            availability_bonus = member.capacity * 0.3
            final_score = min(1.0, match_score + availability_bonus)

            suggestion = TeamMemberSuggestion(
                username=member.username,
                display_name=member.display_name,
                match_score=final_score,
                matching_skills=matching_skills,
                current_workload=1.0 - member.capacity,
            )
            suggestions.append(suggestion)

        # Sort by match score (best matches first)
        suggestions.sort(key=lambda x: x.match_score, reverse=True)
        return suggestions

    def _build_project_overview_content(
        self, project_request: ProjectRequest, breakdowns: List[RequirementBreakdown]
    ) -> str:
        """Build content for project overview page."""
        total_hours = sum(b.estimated_total_hours for b in breakdowns)
        
        content = f"""
<h1>{project_request.project_name}</h1>

<h2>Project Overview</h2>
<p>{project_request.project_description}</p>

<h2>Project Details</h2>
<ul>
<li><strong>Jira Project:</strong> {project_request.jira_project_key}</li>
<li><strong>Confluence Space:</strong> {project_request.confluence_space_key}</li>
<li><strong>Total Estimated Hours:</strong> {total_hours}</li>
<li><strong>Requirements Count:</strong> {len(project_request.requirements)}</li>
<li><strong>Team Size:</strong> {len(project_request.team_members)}</li>
</ul>

<h2>Team Members</h2>
<ul>
"""
        for member in project_request.team_members:
            content += f"<li><strong>{member.display_name}</strong> ({member.username}) - Skills: {', '.join(member.skills)}</li>\n"
        
        content += """</ul>

<h2>Requirements Summary</h2>
<ul>
"""
        for req in project_request.requirements:
            content += f"<li><strong>{req.title}</strong> ({req.priority.value}) - {req.estimated_hours or 'TBD'} hours</li>\n"
        
        content += "</ul>"
        return content

    def _build_technical_requirements_content(
        self, breakdowns: List[RequirementBreakdown]
    ) -> str:
        """Build content for technical requirements page."""
        content = """
<h1>Technical Requirements & Implementation Plan</h1>

<h2>Task Breakdown</h2>
"""
        
        for breakdown in breakdowns:
            content += f"""
<h3>{breakdown.original_requirement}</h3>
<ul>
"""
            for task in breakdown.suggested_tasks:
                content += f"<li><strong>{task['title']}</strong> - {task['description']} (Est: {task['estimated_hours']} hours)</li>\n"
            
            content += "</ul>\n"
        
        return content

    def get_execution_result(self, execution_id: str) -> Optional[ProjectExecutionResult]:
        """Get execution result by ID."""
        return self.execution_history.get(execution_id)

    def list_executions(self) -> List[ProjectExecutionResult]:
        """List all execution results."""
        return list(self.execution_history.values())
