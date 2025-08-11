#!/usr/bin/env python3
"""Example client for AI Scrum Master REST API."""

import asyncio
import json
from typing import Any, Dict

import aiohttp


class AIScumMasterClient:
    """Client for interacting with AI Scrum Master REST API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')

    async def health_check(self) -> Dict[str, Any]:
        """Check API health."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/health") as response:
                return await response.json()

    async def execute_project(self, project_request: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a complete project."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/v1/projects/execute",
                json=project_request
            ) as response:
                return await response.json()

    async def preview_breakdown(self, project_request: Dict[str, Any]) -> Dict[str, Any]:
        """Preview requirement breakdown."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/v1/projects/breakdown",
                json=project_request
            ) as response:
                return await response.json()

    async def get_team_suggestions(self, project_request: Dict[str, Any]) -> Dict[str, Any]:
        """Get team assignment suggestions."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/v1/projects/team-suggestions",
                json=project_request
            ) as response:
                return await response.json()

    async def create_jira_issue(self, **kwargs) -> Dict[str, Any]:
        """Create a single Jira issue."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/v1/jira/issues",
                params=kwargs
            ) as response:
                return await response.json()

    async def create_confluence_page(self, **kwargs) -> Dict[str, Any]:
        """Create a single Confluence page."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/v1/confluence/pages",
                params=kwargs
            ) as response:
                return await response.json()


async def main():
    """Example usage of the AI Scrum Master API."""
    client = AIScumMasterClient()

    print("🔍 Checking API health...")
    health = await client.health_check()
    print(f"Health: {health}")

    # Example project request
    project_request = {
        "project_name": "E-commerce Platform Enhancement",
        "project_description": "Enhance our e-commerce platform with new features including user authentication, product recommendations, and payment processing improvements.",
        "jira_project_key": "SUP",
        "confluence_space_key": "MFS",
        "requirements": [
            {
                "title": "User Authentication System",
                "description": "Implement secure user login, registration, and password reset functionality with OAuth2 support.",
                "priority": "HIGH",
                "estimated_hours": 40,
                "required_skills": ["Python", "OAuth2", "Security", "FastAPI"]
            },
            {
                "title": "Product Recommendation Engine",
                "description": "Build an ML-based recommendation system that suggests products based on user behavior and purchase history.",
                "priority": "MEDIUM",
                "estimated_hours": 60,
                "required_skills": ["Python", "Machine Learning", "Data Science", "SQL"]
            },
            {
                "title": "Payment Processing Integration",
                "description": "Integrate with Stripe and PayPal for secure payment processing with webhook support.",
                "priority": "HIGH",
                "estimated_hours": 32,
                "required_skills": ["Python", "Payment APIs", "Webhooks", "Security"]
            }
        ],
        "team_members": [
            {
                "username": "john.doe",
                "display_name": "John Doe",
                "email": "john.doe@company.com",
                "skills": ["Python", "FastAPI", "OAuth2", "Security"],
                "capacity": 0.8
            },
            {
                "username": "jane.smith",
                "display_name": "Jane Smith",
                "email": "jane.smith@company.com",
                "skills": ["Python", "Machine Learning", "Data Science", "SQL"],
                "capacity": 0.9
            },
            {
                "username": "mike.wilson",
                "display_name": "Mike Wilson",
                "email": "mike.wilson@company.com",
                "skills": ["Python", "Payment APIs", "Webhooks", "JavaScript"],
                "capacity": 0.7
            }
        ],
        "auto_assign": True,
        "create_confluence_docs": True
    }

    print("\n📋 Getting requirement breakdown preview...")
    breakdown = await client.preview_breakdown(project_request)
    print(f"Breakdown preview: {json.dumps(breakdown, indent=2)}")

    print("\n👥 Getting team assignment suggestions...")
    suggestions = await client.get_team_suggestions(project_request)
    print(f"Team suggestions: {json.dumps(suggestions, indent=2)}")

    print("\n🚀 Executing complete project...")
    result = await client.execute_project(project_request)
    print(f"Execution result: {json.dumps(result, indent=2, default=str)}")

    print("\n✅ Example completed!")


if __name__ == "__main__":
    asyncio.run(main())
