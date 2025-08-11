#!/usr/bin/env python3
"""
Example usage of the AI Scrum Master and Project Manager Assistant

This script demonstrates how to set up and use the system with both
Jira and Confluence agents through the orchestrator.
"""

import asyncio
import logging
from datetime import datetime
from src.core.orchestrator import Orchestrator, Command, CommandType
from src.agents.jira_agent import JiraAgent
from src.agents.confluence_agent import ConfluenceAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def setup_system():
    """Set up the complete system with all agents."""
    logger.info("Setting up AI Scrum Master system...")
    
    # Initialize orchestrator
    orchestrator = Orchestrator()
    
    # Initialize agents with MCP server URLs
    # Note: These URLs should point to your actual MCP servers
    jira_agent = JiraAgent("http://localhost:8000")
    confluence_agent = ConfluenceAgent("http://localhost:8001")
    
    # Register agents with orchestrator
    await orchestrator.register_agent("jira_agent", jira_agent)
    await orchestrator.register_agent("confluence_agent", confluence_agent)
    
    # Initialize agents (connect to MCP servers)
    logger.info("Initializing Jira agent...")
    jira_success = await jira_agent.initialize()
    
    logger.info("Initializing Confluence agent...")
    confluence_success = await confluence_agent.initialize()
    
    if jira_success and confluence_success:
        logger.info("All agents initialized successfully!")
    else:
        logger.warning("Some agents failed to initialize")
    
    return orchestrator


async def demonstrate_jira_operations(orchestrator):
    """Demonstrate Jira-related operations."""
    logger.info("=== Demonstrating Jira Operations ===")
    
    # Example 1: Get projects
    command = Command(
        command_id="jira_cmd_001",
        command_type=CommandType.JIRA_PROJECT,
        action="get_projects",
        parameters={"include_archived": False}
    )
    
    logger.info("Executing: Get Jira projects")
    responses = await orchestrator.execute_command(command)
    
    for response in responses:
        if response.success:
            logger.info(f"✅ {response.agent_name}: Retrieved {len(response.data)} projects")
        else:
            logger.error(f"❌ {response.agent_name}: {response.error_message}")
    
    # Example 2: Get issues for a specific project
    command = Command(
        command_id="jira_cmd_002",
        command_type=CommandType.JIRA_ISSUE,
        action="get_issues",
        parameters={"project": "PROJ", "max_results": 5}
    )
    
    logger.info("Executing: Get Jira issues for project PROJ")
    responses = await orchestrator.execute_command(command)
    
    for response in responses:
        if response.success:
            logger.info(f"✅ {response.agent_name}: Retrieved {len(response.data)} issues")
        else:
            logger.error(f"❌ {response.agent_name}: {response.error_message}")


async def demonstrate_confluence_operations(orchestrator):
    """Demonstrate Confluence-related operations."""
    logger.info("=== Demonstrating Confluence Operations ===")
    
    # Example 1: Get space information
    command = Command(
        command_id="confluence_cmd_001",
        command_type=CommandType.CONFLUENCE_SPACE,
        action="get_space",
        parameters={"space_key": "TEAM"}
    )
    
    logger.info("Executing: Get Confluence space TEAM")
    responses = await orchestrator.execute_command(command)
    
    for response in responses:
        if response.success:
            if response.data:
                logger.info(f"✅ {response.agent_name}: Found space '{response.data.name}'")
            else:
                logger.info(f"✅ {response.agent_name}: Space not found")
        else:
            logger.error(f"❌ {response.agent_name}: {response.error_message}")
    
    # Example 2: Search for pages
    command = Command(
        command_id="confluence_cmd_002",
        command_type=CommandType.CONFLUENCE_PAGE,
        action="search_pages",
        parameters={"query": "project documentation", "max_results": 3}
    )
    
    logger.info("Executing: Search Confluence pages for 'project documentation'")
    responses = await orchestrator.execute_command(command)
    
    for response in responses:
        if response.success:
            logger.info(f"✅ {response.agent_name}: Found {len(response.data)} pages")
        else:
            logger.error(f"❌ {response.agent_name}: {response.error_message}")


async def demonstrate_project_management(orchestrator):
    """Demonstrate project management operations that involve multiple agents."""
    logger.info("=== Demonstrating Project Management Operations ===")
    
    # Example: Create a project overview (involves both Jira and Confluence)
    command = Command(
        command_id="pm_cmd_001",
        command_type=CommandType.PROJECT_MANAGEMENT,
        action="create_project_overview",
        parameters={
            "project_key": "PROJ-123",
            "project_name": "AI Assistant Project",
            "space_key": "TEAM",
            "page_title": "Project Overview - AI Assistant"
        }
    )
    
    logger.info("Executing: Create project overview (multi-agent operation)")
    responses = await orchestrator.execute_command(command)
    
    for response in responses:
        if response.success:
            logger.info(f"✅ {response.agent_name}: Operation completed successfully")
        else:
            logger.error(f"❌ {response.agent_name}: {response.error_message}")


async def demonstrate_system_monitoring(orchestrator):
    """Demonstrate system monitoring and status checking."""
    logger.info("=== Demonstrating System Monitoring ===")
    
    # Get system status
    status = orchestrator.get_system_status()
    logger.info(f"System Status:")
    logger.info(f"  - Active agents: {status['total_agents']}")
    logger.info(f"  - Registered agents: {status['registered_agents']}")
    logger.info(f"  - Total commands executed: {status['total_commands']}")
    logger.info(f"  - Cached responses: {status['cached_responses']}")
    logger.info(f"  - Max concurrent commands: {status['max_concurrent_commands']}")
    logger.info(f"  - Available concurrent slots: {status['available_concurrent_slots']}")
    
    # Check command history
    if status['total_commands'] > 0:
        logger.info("Recent commands:")
        for i, command in enumerate(orchestrator.command_history[-3:], 1):
            logger.info(f"  {i}. {command.action} ({command.command_type.value})")


async def main():
    """Main demonstration function."""
    logger.info("🚀 Starting AI Scrum Master Assistant Demo")
    
    try:
        # Set up the system
        orchestrator = await setup_system()
        
        # Demonstrate various operations
        await demonstrate_jira_operations(orchestrator)
        await demonstrate_confluence_operations(orchestrator)
        await demonstrate_project_management(orchestrator)
        await demonstrate_system_monitoring(orchestrator)
        
        # Show final status
        logger.info("\n" + "="*50)
        logger.info("Demo completed successfully!")
        logger.info("="*50)
        
    except Exception as e:
        logger.error(f"Demo failed with error: {e}")
        raise
    finally:
        # Clean shutdown
        if 'orchestrator' in locals():
            logger.info("Shutting down system...")
            await orchestrator.shutdown()
            logger.info("System shutdown complete")


if __name__ == "__main__":
    # Run the demonstration
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        exit(1)
