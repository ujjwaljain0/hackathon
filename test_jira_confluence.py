#!/usr/bin/env python3
"""Test script to check available Jira projects and Confluence spaces."""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_jira_endpoints():
    """Test various Jira endpoints to find available projects."""
    base_url = "https://athonprompt.atlassian.net/rest/api/3"
    auth_token = os.getenv("IRA_MCP_AUTH_TOKEN")  # Note: it's IRA, not JIRA
    
    if not auth_token:
        print("❌ IRA_MCP_AUTH_TOKEN not found in environment")
        return
    
    headers = {"Authorization": auth_token}
    
    # Test different endpoints
    endpoints = [
        "/project",
        "/project/search",
        "/project/category",
        "/serverInfo",
        "/myself",
        "/field",
        "/issuetype"
    ]
    
    # Create SSL context to disable verification
    import ssl
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    
    async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
        print("🔍 Testing Jira endpoints...")
        for endpoint in endpoints:
            try:
                url = f"{base_url}{endpoint}"
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        print(f"✅ {endpoint}: {resp.status}")
                        if endpoint == "/project":
                            if isinstance(data, list):
                                print(f"   📋 Found {len(data)} projects:")
                                for project in data[:5]:  # Show first 5
                                    print(f"      - {project.get('key', 'N/A')}: {project.get('name', 'N/A')}")
                            else:
                                print(f"   📋 Response: {type(data)} - {str(data)[:200]}")
                        elif endpoint == "/serverInfo":
                            print(f"   🖥️  Server: {data.get('serverTitle', 'N/A')}")
                    else:
                        print(f"❌ {endpoint}: {resp.status}")
            except Exception as e:
                print(f"❌ {endpoint}: Error - {str(e)}")

async def test_confluence_endpoints():
    """Test various Confluence endpoints to find available spaces."""
    base_url = "https://athonprompt.atlassian.net/wiki/rest/api"
    auth_token = os.getenv("CONFLUENCE_MCP_AUTH_TOKEN")
    
    if not auth_token:
        print("❌ CONFLUENCE_MCP_AUTH_TOKEN not found in environment")
        return
    
    headers = {"Authorization": auth_token}
    
    # Test different endpoints
    endpoints = [
        "/space",
        "/space/search",
        "/content",
        "/user/current",
        "/settings/lookandfeel"
    ]
    
    # Create SSL context to disable verification
    import ssl
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    
    async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
        print("\n🔍 Testing Confluence endpoints...")
        for endpoint in endpoints:
            try:
                url = f"{base_url}{endpoint}"
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        print(f"✅ {endpoint}: {resp.status}")
                        if endpoint == "/space":
                            if "results" in data:
                                spaces = data["results"]
                                print(f"   📋 Found {len(spaces)} spaces:")
                                for space in spaces[:5]:  # Show first 5
                                    print(f"      - {space.get('key', 'N/A')}: {space.get('name', 'N/A')}")
                            else:
                                print(f"   📋 Response: {type(data)} - {str(data)[:200]}")
                    else:
                        print(f"❌ {endpoint}: {resp.status}")
            except Exception as e:
                print(f"❌ {endpoint}: Error - {str(e)}")

async def main():
    """Main test function."""
    print("🚀 Testing Jira and Confluence API endpoints...")
    print("=" * 60)
    
    await test_jira_endpoints()
    await test_confluence_endpoints()
    
    print("\n" + "=" * 60)
    print("✅ Testing complete!")

if __name__ == "__main__":
    asyncio.run(main())
