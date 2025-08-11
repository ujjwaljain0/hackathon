# AI Scrum Master API

An AI-powered Sprint Creation API that automatically analyzes requirements, creates Jira issues, assigns tasks to team members, and provides Scrum Master insights. Built with FastAPI and integrated with Jira and Confluence using LiteLLM for intelligent task breakdown.

## 🏗️ Architecture Overview

The system is built with a modular, async-ready architecture consisting of:

- **Sprint Creation API**: REST endpoint that processes requirements and creates complete sprints
- **AI Coordinator**: LLM-powered agent that analyzes requirements and breaks them into tasks
- **Jira Integration**: Creates issues, assigns tasks, and manages sprint planning
- **Confluence Integration**: Generates sprint documentation and planning artifacts
- **Async Processing**: Full async/await support for high-performance operations

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Sprint API   │───▶│  AI Coordinator │───▶│ Jira/Confluence │
│   (FastAPI)    │    │   (LiteLLM)     │    │   Integration   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Sprint Results │
                       │ Issues, Docs,   │
                       │  Assignments    │
                       └─────────────────┘
```

## 🚀 Features

- **🧠 AI-Powered Analysis:** Automatically breaks down requirements into actionable tasks
- **🎫 Jira Integration:** Creates issues with proper estimates and assignments  
- **👥 Smart Assignment:** Assigns tasks based on team member skills and capacity
- **📄 Documentation:** Auto-generates sprint planning documentation in Confluence
- **📊 Capacity Planning:** Provides team capacity analysis and recommendations
- **🔄 Real-time Processing:** Async processing for fast response times
- **📚 Interactive API:** Full OpenAPI/Swagger documentation

## 🛠️ Technical Requirements

- **Python**: 3.9+
- **Dependencies**: FastAPI, LiteLLM, aiohttp
- **External Services**: Jira and Confluence (optional)
- **LLM**: OpenAI GPT-4 or compatible model

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai-scrum-master-api
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

## 🔧 Usage

### Sprint Creation API

The main feature is the sprint creation API endpoint that takes user requirements and creates a complete sprint setup:

**Endpoint:** `POST /api/v1/sprints/create`

**Example Request:**
```json
{
  "sprint_name": "Feature Development Sprint 1",
  "sprint_goal": "Implement user authentication and dashboard",
  "duration_weeks": 2,
  "jira_project_key": "SUP",
  "confluence_space_key": "MFS",
  "requirements": "Detailed description of what needs to be implemented...",
  "team_members": [
    {
      "username": "john.doe",
      "display_name": "John Doe",
      "skills": ["React", "TypeScript", "Frontend"],
      "capacity": 1.0
    }
  ],
  "auto_assign_tasks": true,
  "create_documentation": true
}
```

**What it does:**
1. 🤖 AI analyzes requirements and breaks them into actionable tasks
2. 🎫 Creates Jira issues with proper estimates and assignments  
3. 👥 Assigns tasks based on team member skills and capacity
4. 📄 Creates sprint documentation in Confluence
5. 📊 Provides capacity analysis and Scrum Master insights

**Usage:**
```bash
# Start the API server
python run_api_server.py

# Test with example
python sprint_creation_example.py

# API Documentation
# Visit: http://localhost:8000/docs
```

### API Testing

You can test the API using the interactive documentation:

1. **Start the server:**
   ```bash
   python run_api_server.py
   ```

2. **Open API docs:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Test with example:**
   ```bash
   python sprint_creation_example.py
   ```

## 🔧 Environment Configuration

Create a `.env` file with your credentials:

```bash
# Copy the example environment file
cp env.example .env

# Edit with your actual values
# Required:
LITELLM_MODEL=openai/gpt-4o-mini
LITELLM_API_KEY=your-openai-api-key

# Optional (for full Jira/Confluence integration):
JIRA_MCP_URL=https://yourcompany.atlassian.net/rest/api/3
CONFLUENCE_MCP_URL=https://yourcompany.atlassian.net/wiki/rest/api
```

## 🚀 API Endpoints

- **Health Check:** `GET /health`
- **Sprint Creation:** `POST /api/v1/sprints/create` 
- **API Info:** `GET /api/v1/info`
- **Interactive Docs:** `GET /docs`

## 📊 Response Example

```json
{
  "success": true,
  "message": "Sprint 'Feature Sprint 1' created successfully with 5 issues",
  "data": {
    "sprint_name": "Feature Sprint 1",
    "status": "completed", 
    "jira_issues": [
      {
        "key": "SUP-123",
        "title": "Implement user authentication",
        "assignee": "john.doe",
        "url": "https://company.atlassian.net/browse/SUP-123"
      }
    ],
    "total_story_points": 21,
    "estimated_hours": 80,
    "scrum_master_notes": [
      "Sprint is well-balanced across team skills",
      "Consider adding buffer time for testing"
    ]
  }
}
```

## 🎯 Use Cases

- **Sprint Planning:** Automatically create sprint backlogs from high-level requirements
- **Task Breakdown:** Convert complex features into actionable development tasks
- **Team Assignment:** Intelligently assign work based on skills and capacity
- **Capacity Planning:** Analyze team capacity and provide recommendations
- **Documentation:** Generate comprehensive sprint planning documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions and support:
- Check the API documentation at `/docs`
- Review the example usage in `sprint_creation_example.py`
- Create an issue for bugs or feature requests

---

**Built with ❤️ for agile teams who want to focus on building, not planning.**