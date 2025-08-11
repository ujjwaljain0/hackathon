"""Scrum Master agent that orchestrates project management using Jira and Confluence agents."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from ..core.agent_base import BaseAgent
from ..core.types import Command
from .jira_agent import JiraAgent
from .confluence_agent import ConfluenceAgent

logger = logging.getLogger(__name__)


class ScrumMasterAgent(BaseAgent):
    """
    AI Scrum Master agent that manages projects like a real Scrum Master.
    
    Responsibilities:
    - Sprint planning and management
    - Task assignment and tracking
    - Team coordination and communication
    - Backlog grooming and prioritization
    - Sprint ceremonies facilitation
    - Progress monitoring and reporting
    """

    def __init__(self, jira_url: str = None, confluence_url: str = None):
        self.agent_name = "scrum_master_agent"
        self.jira_agent = JiraAgent(jira_url) if jira_url else JiraAgent()
        self.confluence_agent = ConfluenceAgent(confluence_url) if confluence_url else ConfluenceAgent()
        
        # Scrum Master state
        self.current_sprint: Optional[Dict[str, Any]] = None
        self.team_members: List[Dict[str, Any]] = []
        self.project_context: Dict[str, Any] = {}
        self.sprint_goals: List[str] = []
        
        # Scrum metrics tracking
        self.velocity_history: List[int] = []
        self.burndown_data: List[Dict[str, Any]] = []
        
    async def initialize(self) -> bool:
        """Initialize the Scrum Master and underlying agents."""
        logger.info("🏃‍♂️ Initializing Scrum Master Agent...")
        
        jira_ok = await self.jira_agent.initialize()
        confluence_ok = await self.confluence_agent.initialize()
        
        if jira_ok:
            logger.info("✅ Jira Agent connected")
        else:
            logger.warning("⚠️ Jira Agent connection failed")
            
        if confluence_ok:
            logger.info("✅ Confluence Agent connected")
        else:
            logger.warning("⚠️ Confluence Agent connection failed")
        
        logger.info("🎯 Scrum Master Agent ready for project management!")
        return jira_ok or confluence_ok  # At least one should work

    async def execute_command(self, command: Command) -> Any:
        """Execute Scrum Master commands."""
        action = command.action
        params = command.parameters
        
        logger.info(f"🏃‍♂️ Scrum Master executing: {action}")
        
        # Sprint Management Commands
        if action == "start_sprint":
            return await self.start_sprint(**params)
        elif action == "end_sprint":
            return await self.end_sprint(**params)
        elif action == "plan_sprint":
            return await self.plan_sprint(**params)
        elif action == "conduct_standup":
            return await self.conduct_standup(**params)
        elif action == "sprint_retrospective":
            return await self.sprint_retrospective(**params)
            
        # Backlog Management
        elif action == "groom_backlog":
            return await self.groom_backlog(**params)
        elif action == "prioritize_backlog":
            return await self.prioritize_backlog(**params)
        elif action == "estimate_story_points":
            return await self.estimate_story_points(**params)
            
        # Team Management
        elif action == "assign_tasks":
            return await self.assign_tasks(**params)
        elif action == "balance_workload":
            return await self.balance_workload(**params)
        elif action == "track_team_capacity":
            return await self.track_team_capacity(**params)
            
        # Reporting and Monitoring
        elif action == "generate_burndown":
            return await self.generate_burndown(**params)
        elif action == "sprint_report":
            return await self.sprint_report(**params)
        elif action == "team_velocity":
            return await self.calculate_team_velocity(**params)
            
        # Project Setup
        elif action == "setup_project":
            return await self.setup_project(**params)
        elif action == "onboard_team":
            return await self.onboard_team(**params)
            
        else:
            raise ValueError(f"Unknown Scrum Master action: {action}")

    # Sprint Management Methods
    async def start_sprint(
        self, 
        sprint_name: str,
        sprint_goal: str,
        jira_project_key: str,
        confluence_space_key: str,
        duration_weeks: int = 2
    ) -> Dict[str, Any]:
        """Start a new sprint with proper planning."""
        logger.info(f"🚀 Starting sprint: {sprint_name}")
        
        start_date = datetime.now()
        end_date = start_date + timedelta(weeks=duration_weeks)
        
        self.current_sprint = {
            "name": sprint_name,
            "start_date": start_date,
            "end_date": end_date,
            "goal": sprint_goal,
            "jira_project_key": jira_project_key,
            "confluence_space_key": confluence_space_key,
            "status": "active",
            "issues": [],
            "committed_story_points": 0
        }
        
        # Create sprint documentation
        sprint_content = self._create_sprint_documentation(sprint_name, sprint_goal, start_date, end_date)
        
        # Create Confluence page for sprint
        try:
            page = await self.confluence_agent.create_page(
                title=f"Sprint {sprint_name} - Planning & Tracking",
                content=sprint_content,
                space_key=confluence_space_key
            )
            logger.info(f"📄 Created sprint documentation: {page.title}")
        except Exception as e:
            logger.warning(f"⚠️ Could not create sprint documentation: {e}")
        
        self.sprint_goals.append(sprint_goal)
        
        logger.info(f"✅ Sprint {sprint_name} started successfully")
        return {
            "sprint": self.current_sprint,
            "message": f"Sprint {sprint_name} started with goal: {sprint_goal}",
            "duration": f"{duration_weeks} weeks",
            "end_date": end_date.strftime("%Y-%m-%d")
        }

    async def plan_sprint(
        self,
        requirements: List[Dict[str, Any]],
        team_members: List[Dict[str, Any]],
        jira_project_key: str,
        sprint_capacity: int = 40
    ) -> Dict[str, Any]:
        """Conduct sprint planning session."""
        logger.info("📋 Conducting Sprint Planning...")
        
        self.team_members = team_members
        planned_issues = []
        total_story_points = 0
        
        for req in requirements:
            # Estimate story points based on complexity
            story_points = await self._estimate_complexity(req)
            
            if total_story_points + story_points <= sprint_capacity:
                # Find best team member for this requirement
                assignee = await self._assign_best_member(req, team_members)
                
                # Create Jira issue
                try:
                    issue = await self.jira_agent.create_issue(
                        project=jira_project_key,
                        summary=req["title"],
                        description=f"{req['description']}\n\nStory Points: {story_points}\nSprint Planning Notes: Assigned during sprint planning session.",
                        issue_type="Story",
                        priority=req.get("priority", "Medium"),
                        assignee=assignee["username"] if assignee else None,
                        labels=["sprint-planned", f"sp-{story_points}"]
                    )
                    
                    planned_issues.append({
                        "issue_key": issue.key,
                        "title": req["title"],
                        "assignee": assignee["display_name"] if assignee else "Unassigned",
                        "story_points": story_points,
                        "priority": req.get("priority", "Medium")
                    })
                    
                    total_story_points += story_points
                    
                    if self.current_sprint:
                        self.current_sprint["issues"].append(issue.key)
                        self.current_sprint["committed_story_points"] = total_story_points
                    
                    logger.info(f"📝 Created and assigned {issue.key} to {assignee['display_name'] if assignee else 'Unassigned'}")
                    
                except Exception as e:
                    logger.error(f"❌ Failed to create issue for {req['title']}: {e}")
            else:
                logger.info(f"⏭️ Skipping {req['title']} - would exceed sprint capacity")
        
        # Create sprint planning summary
        planning_summary = {
            "sprint_name": self.current_sprint["name"] if self.current_sprint else "Current Sprint",
            "planned_issues": planned_issues,
            "total_story_points": total_story_points,
            "sprint_capacity": sprint_capacity,
            "capacity_utilization": f"{(total_story_points/sprint_capacity)*100:.1f}%",
            "team_assignments": self._summarize_assignments(planned_issues)
        }
        
        logger.info(f"✅ Sprint planning completed: {len(planned_issues)} issues planned")
        return planning_summary

    async def conduct_standup(self, jira_project_key: str) -> Dict[str, Any]:
        """Conduct daily standup and provide status update."""
        logger.info("🗣️ Conducting Daily Standup...")
        
        if not self.current_sprint:
            return {"error": "No active sprint found"}
        
        # Get current sprint issues
        sprint_issues = await self.jira_agent.get_issues(
            project=jira_project_key,
            assignee=None,  # Get all issues
            max_results=50
        )
        
        # Filter issues in current sprint (by labels or creation date)
        current_issues = [
            issue for issue in sprint_issues 
            if any(label in ["sprint-planned"] for label in issue.labels)
        ]
        
        # Analyze progress
        status_summary = {"TODO": 0, "IN_PROGRESS": 0, "DONE": 0, "BLOCKED": 0}
        team_updates = {}
        blocked_issues = []
        
        for issue in current_issues:
            # Count by status
            if issue.status.upper() in ["TO DO", "OPEN", "NEW"]:
                status_summary["TODO"] += 1
            elif issue.status.upper() in ["IN PROGRESS", "WORK IN PROGRESS"]:
                status_summary["IN_PROGRESS"] += 1
            elif issue.status.upper() in ["DONE", "CLOSED", "RESOLVED"]:
                status_summary["DONE"] += 1
            elif issue.status.upper() in ["BLOCKED", "IMPEDIMENT"]:
                status_summary["BLOCKED"] += 1
                blocked_issues.append({"key": issue.key, "summary": issue.summary})
            
            # Group by assignee
            assignee = issue.assignee or "Unassigned"
            if assignee not in team_updates:
                team_updates[assignee] = {"todo": [], "in_progress": [], "done": []}
            
            if issue.status.upper() in ["TO DO", "OPEN", "NEW"]:
                team_updates[assignee]["todo"].append({"key": issue.key, "summary": issue.summary})
            elif issue.status.upper() in ["IN PROGRESS", "WORK IN PROGRESS"]:
                team_updates[assignee]["in_progress"].append({"key": issue.key, "summary": issue.summary})
            elif issue.status.upper() in ["DONE", "CLOSED", "RESOLVED"]:
                team_updates[assignee]["done"].append({"key": issue.key, "summary": issue.summary})
        
        # Calculate sprint progress
        total_issues = len(current_issues)
        completed_issues = status_summary["DONE"]
        progress_percentage = (completed_issues / total_issues * 100) if total_issues > 0 else 0
        
        standup_report = {
            "sprint_name": self.current_sprint["name"],
            "date": datetime.now().strftime("%Y-%m-%d"),
            "sprint_progress": f"{progress_percentage:.1f}%",
            "status_summary": status_summary,
            "team_updates": team_updates,
            "blocked_issues": blocked_issues,
            "total_issues": total_issues,
            "days_remaining": (self.current_sprint["end_date"] - datetime.now()).days,
            "scrum_master_notes": self._generate_standup_insights(status_summary, blocked_issues, progress_percentage)
        }
        
        logger.info(f"✅ Standup completed - {progress_percentage:.1f}% progress, {len(blocked_issues)} blocked")
        return standup_report

    async def assign_tasks(
        self,
        requirements: List[Dict[str, Any]],
        team_members: List[Dict[str, Any]],
        jira_project_key: str
    ) -> Dict[str, Any]:
        """Intelligently assign tasks to team members based on skills and workload."""
        logger.info("👥 Assigning tasks to team members...")
        
        assignments = []
        workload_tracker = {member["username"]: 0 for member in team_members}
        
        for req in requirements:
            best_member = await self._assign_best_member(req, team_members)
            
            if best_member:
                # Create Jira issue
                try:
                    issue = await self.jira_agent.create_issue(
                        project=jira_project_key,
                        summary=req["title"],
                        description=req["description"],
                        issue_type=req.get("issue_type", "Task"),
                        priority=req.get("priority", "Medium"),
                        assignee=best_member["username"],
                        labels=["scrum-assigned"]
                    )
                    
                    assignments.append({
                        "issue_key": issue.key,
                        "title": req["title"],
                        "assignee": best_member["display_name"],
                        "assignee_username": best_member["username"],
                        "priority": req.get("priority", "Medium"),
                        "estimated_hours": req.get("estimated_hours", 8)
                    })
                    
                    workload_tracker[best_member["username"]] += req.get("estimated_hours", 8)
                    
                    logger.info(f"✅ Assigned {issue.key} to {best_member['display_name']}")
                    
                except Exception as e:
                    logger.error(f"❌ Failed to assign {req['title']}: {e}")
        
        return {
            "assignments": assignments,
            "workload_distribution": workload_tracker,
            "total_tasks_assigned": len(assignments),
            "assignment_summary": self._create_assignment_summary(assignments, team_members)
        }

    # Helper Methods
    async def _estimate_complexity(self, requirement: Dict[str, Any]) -> int:
        """Estimate story points based on requirement complexity."""
        estimated_hours = requirement.get("estimated_hours", 8)
        required_skills = len(requirement.get("required_skills", []))
        
        # Simple algorithm for story points
        if estimated_hours <= 4:
            return 1
        elif estimated_hours <= 8:
            return 2 if required_skills <= 2 else 3
        elif estimated_hours <= 16:
            return 3 if required_skills <= 2 else 5
        elif estimated_hours <= 24:
            return 5 if required_skills <= 3 else 8
        else:
            return 8 if required_skills <= 3 else 13

    async def _assign_best_member(
        self,
        requirement: Dict[str, Any],
        team_members: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Find the best team member for a requirement based on skills and capacity."""
        if not team_members:
            return None
        
        required_skills = set(skill.lower() for skill in requirement.get("required_skills", []))
        
        best_member = None
        best_score = -1
        
        for member in team_members:
            member_skills = set(skill.lower() for skill in member.get("skills", []))
            
            # Calculate skill match score
            if required_skills:
                skill_match = len(required_skills.intersection(member_skills)) / len(required_skills)
            else:
                skill_match = 0.5  # Default score when no specific skills required
            
            # Factor in capacity (availability)
            capacity_score = member.get("capacity", 0.8)
            
            # Combined score
            total_score = skill_match * 0.7 + capacity_score * 0.3
            
            if total_score > best_score:
                best_score = total_score
                best_member = member
        
        return best_member

    def _create_sprint_documentation(
        self,
        sprint_name: str,
        sprint_goal: str,
        start_date: datetime,
        end_date: datetime
    ) -> str:
        """Create Confluence content for sprint documentation."""
        return f"""
<h1>Sprint {sprint_name}</h1>

<h2>Sprint Information</h2>
<table>
<tr><td><strong>Sprint Goal:</strong></td><td>{sprint_goal}</td></tr>
<tr><td><strong>Start Date:</strong></td><td>{start_date.strftime('%Y-%m-%d')}</td></tr>
<tr><td><strong>End Date:</strong></td><td>{end_date.strftime('%Y-%m-%d')}</td></tr>
<tr><td><strong>Duration:</strong></td><td>{(end_date - start_date).days} days</td></tr>
</table>

<h2>Sprint Backlog</h2>
<p>Items will be updated as the sprint progresses...</p>

<h2>Daily Standup Notes</h2>
<p>Daily progress and blockers will be tracked here...</p>

<h2>Sprint Retrospective</h2>
<p>Retrospective notes will be added at the end of the sprint...</p>

<h2>Burndown Chart</h2>
<p>Progress tracking and burndown metrics will be updated daily...</p>
"""

    def _generate_standup_insights(
        self,
        status_summary: Dict[str, int],
        blocked_issues: List[Dict[str, str]],
        progress_percentage: float
    ) -> List[str]:
        """Generate Scrum Master insights for standup."""
        insights = []
        
        if blocked_issues:
            insights.append(f"🚫 {len(blocked_issues)} blocked issues need immediate attention")
        
        if progress_percentage < 30 and hasattr(self, 'current_sprint'):
            days_passed = (datetime.now() - self.current_sprint["start_date"]).days
            sprint_duration = (self.current_sprint["end_date"] - self.current_sprint["start_date"]).days
            if days_passed > sprint_duration * 0.5:
                insights.append("⚠️ Sprint may be at risk - consider scope adjustment")
        
        if status_summary["IN_PROGRESS"] > status_summary["TODO"]:
            insights.append("✅ Good work-in-progress flow - team is actively working")
        
        if status_summary["TODO"] > status_summary["IN_PROGRESS"] * 2:
            insights.append("💡 Consider breaking down large items or redistributing work")
        
        return insights

    def _summarize_assignments(self, planned_issues: List[Dict[str, Any]]) -> Dict[str, int]:
        """Summarize task assignments by team member."""
        assignments = {}
        for issue in planned_issues:
            assignee = issue["assignee"]
            if assignee not in assignments:
                assignments[assignee] = 0
            assignments[assignee] += 1
        return assignments

    def _create_assignment_summary(
        self,
        assignments: List[Dict[str, Any]],
        team_members: List[Dict[str, Any]]
    ) -> str:
        """Create a human-readable assignment summary."""
        member_tasks = {}
        for assignment in assignments:
            assignee = assignment["assignee"]
            if assignee not in member_tasks:
                member_tasks[assignee] = []
            member_tasks[assignee].append(assignment["title"])
        
        summary_lines = []
        for member_name, tasks in member_tasks.items():
            summary_lines.append(f"{member_name}: {len(tasks)} tasks ({', '.join(tasks[:2])}{'...' if len(tasks) > 2 else ''})")
        
        return "; ".join(summary_lines)

    async def generate_burndown(self, jira_project_key: str) -> Dict[str, Any]:
        """Generate burndown chart data."""
        if not self.current_sprint:
            return {"error": "No active sprint"}
        
        # Get sprint issues and calculate remaining work
        issues = await self.jira_agent.get_issues(project=jira_project_key, max_results=100)
        
        total_story_points = self.current_sprint.get("committed_story_points", 0)
        completed_points = 0
        
        for issue in issues:
            if issue.status.upper() in ["DONE", "CLOSED", "RESOLVED"]:
                # Extract story points from labels or estimate
                story_points = self._extract_story_points(issue.labels)
                completed_points += story_points
        
        remaining_points = total_story_points - completed_points
        
        # Calculate ideal burndown
        sprint_duration = (self.current_sprint["end_date"] - self.current_sprint["start_date"]).days
        days_elapsed = (datetime.now() - self.current_sprint["start_date"]).days
        ideal_remaining = total_story_points * (1 - days_elapsed / sprint_duration)
        
        return {
            "total_story_points": total_story_points,
            "completed_points": completed_points,
            "remaining_points": remaining_points,
            "ideal_remaining": max(0, ideal_remaining),
            "days_elapsed": days_elapsed,
            "days_remaining": max(0, sprint_duration - days_elapsed),
            "completion_percentage": (completed_points / total_story_points * 100) if total_story_points > 0 else 0
        }

    def _extract_story_points(self, labels: List[str]) -> int:
        """Extract story points from issue labels."""
        for label in labels:
            if label.startswith("sp-"):
                try:
                    return int(label.split("-")[1])
                except (IndexError, ValueError):
                    continue
        return 1  # Default story point value

    async def shutdown(self) -> None:
        """Shutdown the Scrum Master Agent."""
        logger.info("🏃‍♂️ Shutting down Scrum Master Agent...")
        await self.jira_agent.shutdown()
        await self.confluence_agent.shutdown()
        logger.info("✅ Scrum Master Agent shutdown complete")
