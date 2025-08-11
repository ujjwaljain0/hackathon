#!/usr/bin/env python3
"""
Example of using the AI Scrum Master Sprint Creation API.

This script demonstrates how to create a sprint using the REST API endpoint.
"""

import asyncio
import json
from typing import Dict, Any

import aiohttp


async def create_sprint_example():
    """Example of creating a sprint via the API."""
    
    # Sprint creation request data
    sprint_data = {
        "sprint_name": "Feature Development Sprint 1",
        "sprint_goal": "Implement user authentication and basic dashboard functionality",
        "duration_weeks": 2,
        "jira_project_key": "SUP",
        "confluence_space_key": "MFS",
        "requirements": """
We need to implement the following features for our web application:

1. User Authentication System:
   - User registration with email verification
   - Login/logout functionality  
   - Password reset capability
   - JWT token-based authentication
   - User profile management

2. Dashboard Development:
   - Main dashboard layout
   - User greeting and navigation
   - Basic metrics display
   - Responsive design for mobile/desktop

3. Security and Testing:
   - Input validation and sanitization
   - API security middleware
   - Unit tests for authentication
   - Integration tests for dashboard

Technical Requirements:
- Frontend: React with TypeScript
- Backend: Python FastAPI
- Database: PostgreSQL
- Authentication: JWT with refresh tokens
- Testing: Jest for frontend, pytest for backend

The team has experience with these technologies and we need to deliver a working prototype by the end of the sprint.
        """,
        "team_members": [
            {
                "username": "john.doe",
                "display_name": "John Doe",
                "email": "john.doe@company.com",
                "skills": ["React", "TypeScript", "Frontend", "CSS"],
                "capacity": 1.0
            },
            {
                "username": "jane.smith", 
                "display_name": "Jane Smith",
                "email": "jane.smith@company.com",
                "skills": ["Python", "FastAPI", "Backend", "PostgreSQL", "JWT"],
                "capacity": 0.8
            },
            {
                "username": "mike.wilson",
                "display_name": "Mike Wilson", 
                "email": "mike.wilson@company.com",
                "skills": ["Testing", "Jest", "pytest", "QA", "Security"],
                "capacity": 1.0
            }
        ],
        "team_capacity": 0.9,
        "auto_assign_tasks": True,
        "create_documentation": True
    }
    
    # API endpoint
    api_url = "http://localhost:8000/api/v1/sprints/create"
    
    print("🏃‍♂️ Creating sprint via AI Scrum Master API...")
    print(f"Sprint Name: {sprint_data['sprint_name']}")
    print(f"Sprint Goal: {sprint_data['sprint_goal']}")
    print(f"Team Size: {len(sprint_data['team_members'])} members")
    print()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=sprint_data) as response:
                if response.status == 200:
                    result = await response.json()
                    print("✅ Sprint creation successful!")
                    print()
                    
                    # Display results
                    if result.get("success"):
                        data = result.get("data", {})
                        
                        print(f"📋 Sprint: {data.get('sprint_name')}")
                        print(f"📊 Status: {data.get('status')}")
                        print(f"🎫 Jira Issues Created: {len(data.get('jira_issues', []))}")
                        print(f"📄 Documentation Pages: {len(data.get('confluence_pages', []))}")
                        print(f"📈 Total Story Points: {data.get('total_story_points', 0)}")
                        print(f"⏱️ Estimated Hours: {data.get('estimated_hours', 0)}")
                        print()
                        
                        # Show created issues
                        issues = data.get('jira_issues', [])
                        if issues:
                            print("🎫 Created Jira Issues:")
                            for issue in issues:
                                assignee = issue.get('assignee', 'Unassigned')
                                print(f"  • {issue['key']}: {issue['title']} → {assignee}")
                                print(f"    URL: {issue['url']}")
                            print()
                        
                        # Show team assignments
                        assignments = data.get('team_assignments', {})
                        if assignments:
                            print("👥 Team Assignments:")
                            for member, tasks in assignments.items():
                                print(f"  • {member}: {len(tasks)} task(s)")
                                for task in tasks:
                                    print(f"    - {task}")
                            print()
                        
                        # Show AI insights
                        notes = data.get('scrum_master_notes', [])
                        if notes:
                            print("🤖 AI Scrum Master Insights:")
                            for note in notes:
                                print(f"  • {note}")
                            print()
                        
                        # Show capacity analysis
                        capacity = data.get('capacity_analysis')
                        if capacity:
                            print(f"📊 Capacity Analysis: {capacity}")
                            print()
                        
                        # Show any warnings or errors
                        warnings = data.get('warnings', [])
                        if warnings:
                            print("⚠️ Warnings:")
                            for warning in warnings:
                                print(f"  • {warning}")
                            print()
                        
                        errors = data.get('errors', [])
                        if errors:
                            print("❌ Errors:")
                            for error in errors:
                                print(f"  • {error}")
                    else:
                        print(f"❌ Sprint creation failed: {result.get('message')}")
                        if result.get('error'):
                            print(f"Error details: {result['error']}")
                
                else:
                    error_text = await response.text()
                    print(f"❌ HTTP Error {response.status}: {error_text}")
    
    except aiohttp.ClientError as e:
        print(f"❌ Connection error: {e}")
        print("Make sure the API server is running: python run_api_server.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def print_api_usage():
    """Print API usage information."""
    print("🔧 AI Scrum Master Sprint Creation API")
    print("=" * 50)
    print()
    print("📋 Request Format:")
    print("POST /api/v1/sprints/create")
    print()
    print("📊 Required Fields:")
    print("  • sprint_name: Name of the sprint")
    print("  • sprint_goal: Sprint objective")
    print("  • jira_project_key: Jira project (e.g., 'SUP')")
    print("  • requirements: Detailed description of what needs to be done")
    print()
    print("👥 Optional Fields:")
    print("  • team_members: List of available team members with skills")
    print("  • duration_weeks: Sprint duration (default: 2)")
    print("  • team_capacity: Overall team capacity 0.0-1.0 (default: 1.0)")
    print("  • auto_assign_tasks: Auto-assign to team members (default: true)")
    print("  • create_documentation: Create Confluence docs (default: true)")
    print()
    print("🚀 Response:")
    print("  • success: Whether creation was successful")
    print("  • message: Human-readable result message")
    print("  • data: Sprint creation results with issues, assignments, insights")
    print()
    print("💡 Example Usage:")
    print("  python sprint_creation_example.py")
    print()


async def main():
    """Main function."""
    print_api_usage()
    
    response = input("Do you want to run the sprint creation example? (y/n): ")
    if response.lower() in ['y', 'yes']:
        await create_sprint_example()
    else:
        print("👍 Example skipped. You can run it anytime!")


if __name__ == "__main__":
    asyncio.run(main())
