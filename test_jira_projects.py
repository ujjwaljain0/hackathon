#!/usr/bin/env python3
"""Test script to find Jira projects using different methods."""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_jira_project_discovery():
    """Test different methods to find Jira projects."""
    base_url = "https://athonprompt.atlassian.net/rest/api/3"
    auth_token = os.getenv("IRA_MCP_AUTH_TOKEN")
    
    if not auth_token:
        print("❌ IRA_MCP_AUTH_TOKEN not found in environment")
        return
    
    headers = {"Authorization": auth_token}
    
    # Create SSL context to disable verification
    import ssl
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    
    async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
        print("🔍 Testing different Jira project discovery methods...")
        
        # Method 1: Try /project with different parameters
        print("\n1️⃣ Testing /project endpoint with parameters...")
        try:
            url = f"{base_url}/project?expand=lead,description,url,projectKeys"
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(f"   ✅ /project?expand=lead,description,url,projectKeys: {len(data) if isinstance(data, list) else 'Not a list'}")
                    if isinstance(data, list) and len(data) > 0:
                        print(f"   📋 Found {len(data)} projects:")
                        for project in data[:3]:
                            print(f"      - {project.get('key', 'N/A')}: {project.get('name', 'N/A')}")
                else:
                    print(f"   ❌ /project?expand=...: {resp.status}")
        except Exception as e:
            print(f"   ❌ /project?expand=...: Error - {str(e)}")
        
        # Method 2: Try /project/search
        print("\n2️⃣ Testing /project/search endpoint...")
        try:
            url = f"{base_url}/project/search?maxResults=50"
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(f"   ✅ /project/search: {resp.status}")
                    if "values" in data:
                        projects = data["values"]
                        print(f"   📋 Found {len(projects)} projects:")
                        for project in projects[:3]:
                            print(f"      - {project.get('key', 'N/A')}: {project.get('name', 'N/A')}")
                    else:
                        print(f"   📋 Response structure: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                else:
                    print(f"   ❌ /project/search: {resp.status}")
        except Exception as e:
            print(f"   ❌ /project/search: Error - {str(e)}")
        
        # Method 3: Try to get issues and extract project info
        print("\n3️⃣ Testing /search to find projects from issues...")
        try:
            url = f"{base_url}/search?jql=project is not EMPTY&maxResults=10&fields=project"
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(f"   ✅ /search with JQL: {resp.status}")
                    if "issues" in data:
                        issues = data["issues"]
                        print(f"   📋 Found {len(issues)} issues")
                        projects_seen = set()
                        for issue in issues:
                            project = issue.get("fields", {}).get("project", {})
                            project_key = project.get("key", "")
                            if project_key and project_key not in projects_seen:
                                projects_seen.add(project_key)
                                print(f"      - Project from issue: {project_key}: {project.get('name', 'N/A')}")
                    else:
                        print(f"   📋 Response structure: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                else:
                    print(f"   ❌ /search with JQL: {resp.status}")
        except Exception as e:
            print(f"   ❌ /search with JQL: Error - {str(e)}")
        
        # Method 4: Try /myself to check user permissions
        print("\n4️⃣ Testing /myself to check user permissions...")
        try:
            url = f"{base_url}/myself"
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(f"   ✅ /myself: {resp.status}")
                    print(f"   👤 User: {data.get('displayName', 'N/A')} ({data.get('emailAddress', 'N/A')})")
                    print(f"   🔑 Account ID: {data.get('accountId', 'N/A')}")
                else:
                    print(f"   ❌ /myself: {resp.status}")
        except Exception as e:
            print(f"   ❌ /myself: Error - {str(e)}")

async def main():
    """Main test function."""
    print("🚀 Testing Jira project discovery methods...")
    print("=" * 70)
    
    await test_jira_project_discovery()
    
    print("\n" + "=" * 70)
    print("✅ Testing complete!")
    print("\n💡 If no projects are found, check:")
    print("   1. Your Jira web interface for project keys")
    print("   2. API token permissions (needs 'Read' access to projects)")
    print("   3. Project visibility settings")

if __name__ == "__main__":
    asyncio.run(main())
