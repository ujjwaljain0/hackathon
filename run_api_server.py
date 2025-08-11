#!/usr/bin/env python3
"""Run the AI Scrum Master REST API server."""

import logging
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Run the API server."""
    logger.info("🚀 Starting AI Scrum Master REST API Server...")
    
    # Check for required environment variables
    required_vars = [
        "LITELLM_MODEL",
        "LITELLM_API_KEY",
        "JIRA_MCP_URL",
        "CONFLUENCE_MCP_URL",
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please check your .env file configuration.")
        sys.exit(1)
    
    logger.info("✅ Environment variables validated")
    logger.info(f"🤖 LLM Model: {os.getenv('LITELLM_MODEL')}")
    logger.info(f"🎫 Jira URL: {os.getenv('JIRA_MCP_URL')}")
    logger.info(f"📄 Confluence URL: {os.getenv('CONFLUENCE_MCP_URL')}")
    
    # Run the server
    uvicorn.run(
        "src.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True,
    )


if __name__ == "__main__":
    main()
