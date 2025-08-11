#!/usr/bin/env python3
"""AI Scrum Master and Project Manager Assistant.

This is the main application that orchestrates Jira and Confluence operations
using Google Agent Development Kit style coordination with LiteLLM.
"""

import asyncio
import logging

from src.core.google_agent_development_kit_coordinator import (
    GoogleAgentDevelopmentKitCoordinator,
)
from src.core.types import Command, CommandType
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main():
    """Main AI Scrum Master application entry point."""
    logger.info("🚀 Starting AI Scrum Master Assistant")
    
    # Initialize the coordinator with Jira and Confluence agents
    coord = GoogleAgentDevelopmentKitCoordinator()
    ok = await coord.initialize()
    if not ok:
        logger.warning("Some backend services failed to initialize - running in degraded mode")

    # Demonstrate AI-powered project management operations
    logger.info("📝 Creating project documentation...")
    responses = await coord.chat_execute("Create a project overview page in Confluence space MFS titled 'AI Scrum Master Overview'.")
    for r in responses:
        if r.success:
            logger.info("✅ %s: Success", r.agent_name)
        else:
            logger.error("❌ %s: %s", r.agent_name, r.error_message)

    # Demonstrate structured command execution
    logger.info("🔍 Searching for project information...")
    cmd = Command(
        command_id="project_info_001",
        command_type=CommandType.CONFLUENCE_PAGE,
        action="get_page",
        parameters={"title": "AI Scrum Master Overview", "space_key": "MFS"},
    )
    results = await coord.execute_command(cmd)
    for r in results:
        if r.success:
            logger.info("✅ %s: Found project information", r.agent_name)
        else:
            logger.error("❌ %s: %s", r.agent_name, r.error_message)

    logger.info("🎯 AI Scrum Master session completed")
    await coord.shutdown()


if __name__ == "__main__":
    asyncio.run(main())