"""FastAPI server for AI Scrum Master REST API."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from .models import (
    ErrorResponse,
    GeneratedJiraIssue,
    HealthCheck,
    ProjectExecutionResponse,
    ProjectRequest,
    RequirementBreakdown,
    SprintCreationRequest,
    SprintCreationResponse,
    SprintCreationResult,
    TeamMemberSuggestion,
)

# Chat interface models
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Chat session ID")

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI Scrum Master response")
    session_id: str = Field(..., description="Chat session ID")
    timestamp: datetime = Field(default_factory=datetime.now)
from .project_orchestrator import ProjectOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Scrum Master API",
    description="REST API for automated project management using AI agents for Jira and Confluence",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global orchestrator instance
orchestrator: Optional[ProjectOrchestrator] = None


@app.on_event("startup")
async def startup_event():
    """Initialize the project orchestrator on startup."""
    global orchestrator
    logger.info("🚀 Starting AI Scrum Master API...")
    
    orchestrator = ProjectOrchestrator()
    init_success = await orchestrator.initialize()
    
    if init_success:
        logger.info("✅ AI Scrum Master API started successfully")
    else:
        logger.warning("⚠️ API started but some services may be unavailable")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    global orchestrator
    logger.info("🛑 Shutting down AI Scrum Master API...")
    
    if orchestrator:
        await orchestrator.shutdown()
    
    logger.info("✅ AI Scrum Master API shutdown complete")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"❌ Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            details=str(exc)
        ).dict()
    )


# Chat interface endpoint
@app.get("/chat", response_class=HTMLResponse)
async def chat_interface():
    """Serve the chat interface HTML."""
    try:
        with open("chat_interface.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Chat interface not found</h1>", status_code=404)

# Health check endpoint
@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Check API and service health."""
    global orchestrator
    
    services = {
        "api": True,
        "jira": False,
        "confluence": False,
    }
    
    if orchestrator:
        services["jira"] = orchestrator.coordinator.jira_available
        services["confluence"] = orchestrator.coordinator.confluence_available
    
    overall_status = "healthy" if all(services.values()) else "degraded"
    
    return HealthCheck(
        status=overall_status,
        services=services,
    )


# Main project execution endpoint
@app.post("/api/v1/projects/execute", response_model=ProjectExecutionResponse)
async def execute_project(project_request: ProjectRequest):
    """
    Execute a complete project request.
    
    This endpoint will:
    1. Break down requirements using AI
    2. Create Confluence documentation (if enabled)
    3. Create Jira issues
    4. Assign tasks to team members (if enabled)
    
    Returns execution results with created issues and pages.
    """
    global orchestrator
    
    if not orchestrator:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Orchestrator not available"
        )
    
    logger.info(f"📥 Received project execution request: {project_request.project_name}")
    
    try:
        result = await orchestrator.execute_project(project_request)
        
        if result.status == "completed":
            return ProjectExecutionResponse(
                success=True,
                message=f"Project '{project_request.project_name}' executed successfully",
                data=result
            )
        else:
            return ProjectExecutionResponse(
                success=False,
                message=f"Project execution failed: {', '.join(result.errors)}",
                data=result,
                error=", ".join(result.errors) if result.errors else "Unknown error"
            )
    
    except Exception as e:
        logger.error(f"❌ Project execution error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Project execution failed: {str(e)}"
        )


# Get execution result by ID
@app.get("/api/v1/projects/executions/{execution_id}")
async def get_execution_result(execution_id: str):
    """Get execution result by ID."""
    global orchestrator
    
    if not orchestrator:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Orchestrator not available"
        )
    
    result = orchestrator.get_execution_result(execution_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found"
        )
    
    return result


# List all executions
@app.get("/api/v1/projects/executions")
async def list_executions():
    """List all project executions."""
    global orchestrator
    
    if not orchestrator:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Orchestrator not available"
        )
    
    return orchestrator.list_executions()


# Requirement breakdown endpoint (for preview)
@app.post("/api/v1/projects/breakdown", response_model=List[RequirementBreakdown])
async def preview_requirement_breakdown(project_request: ProjectRequest):
    """
    Preview how requirements would be broken down without executing.
    
    Useful for clients to see suggested task breakdown and assignments
    before executing the full project.
    """
    global orchestrator
    
    if not orchestrator:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Orchestrator not available"
        )
    
    logger.info(f"📋 Generating requirement breakdown preview for: {project_request.project_name}")
    
    try:
        breakdowns = await orchestrator._break_down_requirements(project_request)
        return breakdowns
    
    except Exception as e:
        logger.error(f"❌ Breakdown preview error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Breakdown preview failed: {str(e)}"
        )


# Team assignment suggestions endpoint
@app.post("/api/v1/projects/team-suggestions")
async def get_team_suggestions(project_request: ProjectRequest):
    """
    Get team assignment suggestions for each requirement.
    
    Returns suggested assignees based on skills and capacity
    without creating any Jira issues.
    """
    global orchestrator
    
    if not orchestrator:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Orchestrator not available"
        )
    
    logger.info(f"👥 Generating team suggestions for: {project_request.project_name}")
    
    try:
        suggestions = {}
        for requirement in project_request.requirements:
            suggestions[requirement.title] = orchestrator._suggest_assignees(
                requirement, project_request.team_members
            )
        
        return suggestions
    
    except Exception as e:
        logger.error(f"❌ Team suggestions error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Team suggestions failed: {str(e)}"
        )


# Simple Jira issue creation endpoint
@app.post("/api/v1/jira/issues")
async def create_jira_issue(
    project_key: str,
    summary: str,
    description: str = "",
    issue_type: str = "Task",
    priority: str = "Medium",
    assignee: Optional[str] = None,
):
    """Create a single Jira issue."""
    global orchestrator
    
    if not orchestrator:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Orchestrator not available"
        )
    
    if not orchestrator.coordinator.jira_available:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Jira service not available"
        )
    
    logger.info(f"🎫 Creating Jira issue: {summary}")
    
    try:
        prompt = (
            f"Create a Jira issue in project '{project_key}' "
            f"with summary '{summary}' "
            f"and description '{description}' "
            f"Set priority to '{priority}' and issue type to '{issue_type}'"
        )
        
        if assignee:
            prompt += f" and assign to '{assignee}'"
        
        responses = await orchestrator.coordinator.chat_execute(prompt)
        
        for response in responses:
            if response.success and hasattr(response.data, 'key'):
                return {
                    "success": True,
                    "issue": {
                        "key": response.data.key,
                        "summary": response.data.summary,
                        "assignee": response.data.assignee,
                        "url": f"https://athonprompt.atlassian.net/browse/{response.data.key}"
                    }
                }
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create Jira issue"
        )
    
    except Exception as e:
        logger.error(f"❌ Jira issue creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Jira issue creation failed: {str(e)}"
        )


# Simple Confluence page creation endpoint
@app.post("/api/v1/confluence/pages")
async def create_confluence_page(
    space_key: str,
    title: str,
    content: str,
    parent_id: Optional[str] = None,
):
    """Create a single Confluence page."""
    global orchestrator
    
    if not orchestrator:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Orchestrator not available"
        )
    
    if not orchestrator.coordinator.confluence_available:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Confluence service not available"
        )
    
    logger.info(f"📄 Creating Confluence page: {title}")
    
    try:
        prompt = (
            f"Create a Confluence page in space '{space_key}' "
            f"titled '{title}' "
            f"with content: {content}"
        )
        
        responses = await orchestrator.coordinator.chat_execute(prompt)
        
        for response in responses:
            if response.success and hasattr(response.data, 'id'):
                return {
                    "success": True,
                    "page": {
                        "id": response.data.id,
                        "title": response.data.title,
                        "space_key": response.data.space_key,
                        "url": f"https://athonprompt.atlassian.net/wiki/spaces/{response.data.space_key}/pages/{response.data.id}"
                    }
                }
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create Confluence page"
        )
    
    except Exception as e:
        logger.error(f"❌ Confluence page creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Confluence page creation failed: {str(e)}"
        )


# Sprint creation endpoint
@app.post("/api/v1/sprints/create", response_model=SprintCreationResponse)
async def create_sprint(sprint_request: SprintCreationRequest):
    """
    Create a new sprint with AI assistance.
    
    This endpoint will:
    1. Analyze the requirements using AI Scrum Master
    2. Break down work into appropriate tasks
    3. Create Jira issues with proper estimates
    4. Set up sprint in Jira (if possible)
    5. Assign tasks to team members based on skills and capacity
    6. Create sprint documentation in Confluence
    7. Provide Scrum Master insights and recommendations
    
    Returns comprehensive sprint setup results.
    """
    global orchestrator
    
    if not orchestrator:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Orchestrator not available"
        )
    
    logger.info(f"🏃‍♂️ Creating sprint: {sprint_request.sprint_name}")
    
    try:
        # Create comprehensive prompt for AI Scrum Master
        team_info = ""
        if sprint_request.team_members:
            team_info = f"\nTeam members available:\n"
            for member in sprint_request.team_members:
                skills_str = ", ".join(member.skills) if member.skills else "No specific skills listed"
                team_info += f"- {member.display_name} ({member.username}): {skills_str}, capacity: {member.capacity * 100}%\n"
        
        prompt = f"""
As an AI Scrum Master, help me create a sprint with the following information:

Sprint Name: {sprint_request.sprint_name}
Sprint Goal: {sprint_request.sprint_goal}
Duration: {sprint_request.duration_weeks} weeks
Project: {sprint_request.jira_project_key}
Team Capacity: {sprint_request.team_capacity * 100}%

Requirements and Context:
{sprint_request.requirements}

{team_info}

Please help me:
1. Break down the requirements into specific, actionable Jira issues
2. Estimate story points for each issue
3. {"Assign tasks to appropriate team members based on their skills and capacity" if sprint_request.auto_assign_tasks else "Suggest appropriate assignees"}
4. {"Create sprint planning documentation" if sprint_request.create_documentation else "Skip documentation creation"}
5. Provide insights on sprint capacity and planning
6. Create the actual Jira issues in project {sprint_request.jira_project_key}

Focus on creating well-defined, achievable tasks that fit within the sprint timeframe.
"""
        
        # Execute with AI Scrum Master
        responses = await orchestrator.coordinator.chat_execute(prompt)
        
        # Process responses and extract results
        result = SprintCreationResult(
            sprint_name=sprint_request.sprint_name,
            status="completed",
        )
        
        for response in responses:
            if response.success:
                if isinstance(response.data, dict):
                    # Extract issue information if available
                    if "issues" in response.data:
                        for issue_data in response.data.get("issues", []):
                            if hasattr(issue_data, 'key'):
                                result.jira_issues.append(GeneratedJiraIssue(
                                    key=issue_data.key,
                                    title=issue_data.summary,
                                    description=getattr(issue_data, 'description', ''),
                                    assignee=getattr(issue_data, 'assignee', None),
                                    priority=getattr(issue_data, 'priority', 'Medium'),
                                    issue_type=getattr(issue_data, 'issue_type', 'Task'),
                                    estimated_hours=getattr(issue_data, 'estimated_hours', None),
                                    url=f"https://athonprompt.atlassian.net/browse/{issue_data.key}"
                                ))
                    
                    # Extract other planning information
                    if "story_points" in response.data:
                        result.total_story_points = response.data.get("story_points", 0)
                    if "estimated_hours" in response.data:
                        result.estimated_hours = response.data.get("estimated_hours", 0)
                    if "assignments" in response.data:
                        result.team_assignments = response.data.get("assignments", {})
                    if "scrum_master_notes" in response.data:
                        result.scrum_master_notes = response.data.get("scrum_master_notes", [])
                    if "capacity_analysis" in response.data:
                        result.capacity_analysis = response.data.get("capacity_analysis", "")
                
                # Add general success message if we got a string response
                elif isinstance(response.data, str):
                    result.scrum_master_notes.append(response.data)
            else:
                result.errors.append(f"{response.agent_name}: {response.error_message}")
        
        # If we have errors but also some success, mark as partial
        if result.errors and (result.jira_issues or result.scrum_master_notes):
            result.status = "partial"
        elif result.errors:
            result.status = "failed"
        
        # Generate response
        if result.status == "completed":
            return SprintCreationResponse(
                success=True,
                message=f"Sprint '{sprint_request.sprint_name}' created successfully with {len(result.jira_issues)} issues",
                data=result
            )
        elif result.status == "partial":
            return SprintCreationResponse(
                success=True,
                message=f"Sprint '{sprint_request.sprint_name}' partially created with some issues",
                data=result
            )
        else:
            return SprintCreationResponse(
                success=False,
                message=f"Failed to create sprint '{sprint_request.sprint_name}'",
                data=result,
                error="; ".join(result.errors)
            )
    
    except Exception as e:
        logger.error(f"❌ Sprint creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Sprint creation failed: {str(e)}"
        )


# Chat endpoint for direct interaction with AI Scrum Master
@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_with_scrum_master(chat_message: ChatMessage):
    """
    Chat directly with the AI Scrum Master.
    
    This endpoint allows natural language interaction with the AI Scrum Master
    for sprint planning, task breakdown, team coordination, and general
    Scrum guidance.
    """
    global orchestrator
    
    if not orchestrator:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Orchestrator not available"
        )
    
    # Generate session ID if not provided
    session_id = chat_message.session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    logger.info(f"💬 Chat request: {chat_message.message[:100]}...")
    
    try:
        # Process with AI Scrum Master
        responses = await orchestrator.coordinator.chat_execute(chat_message.message)
        
        # Combine all responses into a single chat response
        combined_response = ""
        for response in responses:
            if response.success:
                if isinstance(response.data, str):
                    combined_response += f"{response.data}\n\n"
                elif isinstance(response.data, dict):
                    # Format structured data nicely
                    if "issues" in response.data:
                        combined_response += "🎫 **Created Issues:**\n"
                        for issue in response.data.get("issues", []):
                            combined_response += f"- {issue.get('key', 'N/A')}: {issue.get('summary', 'No title')}\n"
                        combined_response += "\n"
                    
                    if "scrum_master_notes" in response.data:
                        combined_response += "🤖 **Scrum Master Insights:**\n"
                        for note in response.data.get("scrum_master_notes", []):
                            combined_response += f"- {note}\n"
                        combined_response += "\n"
                    
                    if "assignments" in response.data:
                        combined_response += "👥 **Team Assignments:**\n"
                        for member, tasks in response.data.get("assignments", {}).items():
                            combined_response += f"- {member}: {len(tasks)} task(s)\n"
                        combined_response += "\n"
                else:
                    combined_response += f"{response.data}\n\n"
            else:
                combined_response += f"❌ {response.agent_name}: {response.error_message}\n\n"
        
        # Clean up the response
        combined_response = combined_response.strip()
        if not combined_response:
            combined_response = "🤖 I'm here to help with your Scrum processes! Please let me know what you need assistance with."
        
        return ChatResponse(
            response=combined_response,
            session_id=session_id,
            timestamp=datetime.now()
        )
    
    except Exception as e:
        logger.error(f"❌ Chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed: {str(e)}"
        )


# API info endpoint
@app.get("/api/v1/info")
async def api_info():
    """Get API information."""
    return {
        "name": "AI Scrum Master API",
        "version": "1.0.0",
        "description": "REST API for automated project management using AI agents",
        "endpoints": {
            "health": "/health",
            "chat_interface": "/chat",
            "create_sprint": "/api/v1/sprints/create",
            "execute_project": "/api/v1/projects/execute",
            "preview_breakdown": "/api/v1/projects/breakdown",
            "team_suggestions": "/api/v1/projects/team-suggestions",
            "create_jira_issue": "/api/v1/jira/issues",
            "create_confluence_page": "/api/v1/confluence/pages",
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
