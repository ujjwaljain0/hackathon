#!/usr/bin/env python3
"""Demo script to test the AI Scrum Master REST API."""

import asyncio
import json
import sys
from datetime import datetime

import aiohttp


async def test_api_endpoints():
    """Test the main API endpoints."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing AI Scrum Master REST API")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        
        # Test 1: Health check
        print("\n1️⃣ Testing health check...")
        try:
            async with session.get(f"{base_url}/health") as response:
                if response.status == 200:
                    health_data = await response.json()
                    print(f"✅ Health check passed: {health_data['status']}")
                    print(f"   Services: {health_data['services']}")
                else:
                    print(f"❌ Health check failed: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Cannot connect to API server: {e}")
            print("💡 Make sure to start the server first: python3 run_api_server.py")
            return False
        
        # Test 2: API info
        print("\n2️⃣ Testing API info...")
        try:
            async with session.get(f"{base_url}/api/v1/info") as response:
                if response.status == 200:
                    info_data = await response.json()
                    print(f"✅ API Info: {info_data['name']} v{info_data['version']}")
                else:
                    print(f"❌ API info failed: {response.status}")
        except Exception as e:
            print(f"❌ API info error: {e}")
        
        # Test 3: Team suggestions (preview mode)
        print("\n3️⃣ Testing team suggestions (preview mode)...")
        sample_project = {
            "project_name": "API Test Project",
            "project_description": "Testing the AI Scrum Master API functionality",
            "jira_project_key": "SUP",
            "confluence_space_key": "MFS",
            "requirements": [
                {
                    "title": "API Authentication",
                    "description": "Implement secure API authentication with JWT tokens",
                    "priority": "HIGH",
                    "estimated_hours": 16,
                    "required_skills": ["Python", "Security", "JWT", "FastAPI"]
                },
                {
                    "title": "Database Integration",
                    "description": "Set up database models and migrations",
                    "priority": "MEDIUM", 
                    "estimated_hours": 12,
                    "required_skills": ["Python", "SQL", "Database Design"]
                }
            ],
            "team_members": [
                {
                    "username": "alice.johnson",
                    "display_name": "Alice Johnson",
                    "email": "alice@company.com",
                    "skills": ["Python", "FastAPI", "Security", "JWT"],
                    "capacity": 0.8
                },
                {
                    "username": "bob.smith",
                    "display_name": "Bob Smith", 
                    "email": "bob@company.com",
                    "skills": ["Python", "SQL", "Database Design", "PostgreSQL"],
                    "capacity": 0.9
                }
            ],
            "auto_assign": True,
            "create_confluence_docs": True
        }
        
        try:
            async with session.post(
                f"{base_url}/api/v1/projects/team-suggestions",
                json=sample_project
            ) as response:
                if response.status == 200:
                    suggestions = await response.json()
                    print("✅ Team suggestions generated successfully")
                    for req_title, assignees in suggestions.items():
                        print(f"   📋 {req_title}:")
                        for assignee in assignees[:2]:  # Show top 2 suggestions
                            print(f"      👤 {assignee['display_name']} (score: {assignee['match_score']:.2f})")
                else:
                    print(f"❌ Team suggestions failed: {response.status}")
                    error_text = await response.text()
                    print(f"   Error: {error_text}")
        except Exception as e:
            print(f"❌ Team suggestions error: {e}")
        
        # Test 4: Requirement breakdown (preview mode)
        print("\n4️⃣ Testing requirement breakdown (preview mode)...")
        try:
            async with session.post(
                f"{base_url}/api/v1/projects/breakdown",
                json=sample_project
            ) as response:
                if response.status == 200:
                    breakdown = await response.json()
                    print("✅ Requirement breakdown generated successfully")
                    for item in breakdown:
                        print(f"   📋 {item['original_requirement']}")
                        print(f"      Tasks: {len(item['suggested_tasks'])}")
                        print(f"      Hours: {item['estimated_total_hours']}")
                else:
                    print(f"❌ Requirement breakdown failed: {response.status}")
                    error_text = await response.text()
                    print(f"   Error: {error_text}")
        except Exception as e:
            print(f"❌ Requirement breakdown error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 API Demo Test Completed!")
    print("\n💡 To run the full project execution test:")
    print("   python3 examples/client_example.py")
    print("\n📚 API Documentation available at:")
    print("   http://localhost:8000/docs")
    
    return True


async def main():
    """Main demo function."""
    success = await test_api_endpoints()
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
