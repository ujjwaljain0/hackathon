# AI Scrum Master and Project Manager Assistant (Google Agent Development Kit style)

A comprehensive backend system for an AI-powered Scrum Master and Project Manager assistant that integrates with Jira, Confluence, and other project management tools via their REST APIs, orchestrated in a Google Agent Development Kit style using LiteLLM for the model interface.

## 🏗️ Architecture Overview

The system is built with a modular, async-ready architecture consisting of:

- **Core Orchestrator**: Central command router and coordinator
- **ADK-style Coordinator**: LLM tool-calling orchestration (via LiteLLM) that selects Jira/Confluence tools
- **Sub-Agents**: Specialized agents for different services (Jira, Confluence, etc.)
- **REST API Integration**: Direct integration with Atlassian REST APIs
- **Async Processing**: Full async/await support for high-performance operations

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input   │───▶│   Orchestrator  │───▶│  Sub-Agents    │
│   (Commands)   │    │                 │    │                │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  Command Cache  │    │   MCP Servers   │
                       │  & History     │    │  (Jira, etc.)   │
                       └─────────────────┘    └─────────────────┘
```

## 🚀 Features

### Core Orchestrator
- **Intelligent Command Routing**: Automatically routes commands to appropriate sub-agents
- **Async Execution**: Concurrent processing of multiple commands
- **Response Aggregation**: Combines responses from multiple agents
- **Command History**: Tracks all executed commands and responses
- **Caching System**: Intelligent caching for improved performance
- **Error Handling**: Comprehensive error handling and recovery

### Jira Agent
- **Issue Management**: Create, read, update, delete Jira issues
- **Project Operations**: Manage Jira projects and configurations
- **Sprint Management**: Handle sprint planning and tracking
- **Advanced Search**: JQL-based issue searching
- **Caching**: Smart caching for frequently accessed data

### Confluence Agent
- **Page Management**: Create, read, update, delete Confluence pages
- **Space Operations**: Manage Confluence spaces and hierarchies
- **Content Search**: Full-text search across pages and spaces
- **Attachment Handling**: Manage page attachments and files
- **Version Control**: Track page versions and history

## 🛠️ Technical Requirements

- **Python**: 3.9+
- **Async Support**: Full asyncio compatibility
- **Dependencies**: aiohttp for HTTP client operations; LiteLLM for ADK-style orchestration
- **MCP Servers**: Remote or local MCP servers for backend integration

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai-scrum-master-assistant
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run examples with src on PYTHONPATH** (or install as a package):
   ```bash
   export PYTHONPATH=.
   python example_usage.py
   ```

## 🔧 Usage

### Basic Setup (Classic Orchestrator)

```python
import asyncio
from src.core.orchestrator import Orchestrator
from src.agents.jira_agent import JiraAgent
from src.agents.confluence_agent import ConfluenceAgent

async def main():
    # Initialize orchestrator
    orchestrator = Orchestrator()
    
    # Initialize and register agents
    jira_agent = JiraAgent("http://localhost:8000")
    confluence_agent = ConfluenceAgent("http://localhost:8001")
    
    # Register agents with orchestrator
    await orchestrator.register_agent("jira_agent", jira_agent)
    await orchestrator.register_agent("confluence_agent", confluence_agent)
    
    # Initialize agents
    await jira_agent.initialize()
    await confluence_agent.initialize()
    
    return orchestrator

# Run the system
orchestrator = asyncio.run(main())
```

### Executing Commands

```python
from src.core.types import Command, CommandType

# Create a command
command = Command(
    command_id="cmd_001",
    command_type=CommandType.JIRA_ISSUE,
    action="get_issues",
    parameters={"project": "PROJ-123", "status": "In Progress"}
)

# Execute the command
responses = await orchestrator.execute_command(command)

# Process responses
for response in responses:
    if response.success:
        print(f"Agent {response.agent_name}: {response.data}")
    else:
        print(f"Agent {response.agent_name} failed: {response.error_message}")
```

## 🔌 Adding New Sub-Agents

### 1. Create Agent Class

Create a new agent class following the established pattern:

```python
class NewServiceAgent:
    def __init__(self, mcp_server_url: str):
        self.mcp_client = MCPClient(mcp_server_url, "new_service")
        self.agent_name = "new_service_agent"
        # ... other initialization
    
    async def initialize(self) -> bool:
        # Initialize connection to MCP server
        pass
    
    async def execute_command(self, command: Command) -> Any:
        # Handle commands specific to this service
        pass
    
    async def shutdown(self) -> None:
        # Clean shutdown
        pass
```

### 2. Register with Orchestrator

```python
new_agent = NewServiceAgent("http://localhost:8002")
await orchestrator.register_agent("new_service_agent", new_agent)
await new_agent.initialize()
```

### 3. Update Command Routing

Modify the `_route_command` method in the orchestrator to handle new command types:

```python
def _route_command(self, command: Command) -> List[str]:
    # ... existing routing logic ...
    
    elif command.command_type == CommandType.NEW_SERVICE:
        if 'new_service_agent' in self.agents:
            target_agents.append('new_service_agent')
    
    return target_agents
```

## 🌐 Connecting to MCP Servers

### MCP Server Setup

1. **Install MCP Server**: Set up MCP servers for your services
2. **Configure Endpoints**: Ensure proper API endpoints are available
3. **Authentication**: Set up proper authentication mechanisms
4. **Health Checks**: Implement `/health` endpoints for connection testing

### MCP Client Configuration

```python
# In your agent class
self.mcp_client = MCPClient(
    mcp_server_url="http://your-mcp-server:port",
    mcp_server_type="your_service"
)

# Connect to server
await self.mcp_client.connect()
```

### Custom MCP Integration

For custom MCP servers, extend the `MCPClient` class:

```python
class CustomMCPClient(MCPClient):
    async def custom_method(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return await self._make_request("/custom/endpoint", "POST", data)
```

## 📊 Monitoring and Debugging

### System Status

```python
# Get system status
status = orchestrator.get_system_status()
print(f"Active agents: {status['total_agents']}")
print(f"Total commands: {status['total_commands']}")
```

### Command History

```python
# Check command status
command_status = await orchestrator.get_command_status("cmd_001")
if command_status:
    print(f"Command responses: {command_status['responses']}")
```

### Logging

The system uses Python's built-in logging with configurable levels:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔒 Security Considerations

- **Authentication**: Implement proper authentication for MCP servers
- **Authorization**: Use role-based access control for sensitive operations
- **Input Validation**: Validate all command parameters
- **Rate Limiting**: Implement rate limiting for API calls
- **Secure Communication**: Use HTTPS for all external communications

## 🚀 Performance Optimization

- **Connection Pooling**: Reuse HTTP connections where possible
- **Caching**: Implement intelligent caching strategies
- **Async Operations**: Use async/await for I/O-bound operations
- **Batch Operations**: Group related operations when possible
- **Resource Management**: Proper cleanup of resources and connections

## 🧪 Testing

### Unit Tests

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_jira_agent():
    agent = JiraAgent()
    # Test agent functionality
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_orchestrator_integration():
    orchestrator = Orchestrator()
    # Test full system integration
```

## 📚 API Reference

### Orchestrator Methods

- `register_agent(agent_name, agent_instance)`: Register a sub-agent
- `execute_command(command)`: Execute a command and return responses
- `get_command_status(command_id)`: Get status of a specific command
- `get_system_status()`: Get overall system status
- `shutdown()`: Gracefully shutdown the system

### Command Structure

```python
@dataclass
class Command:
    command_id: str
    command_type: CommandType
    action: str
    parameters: Dict[str, Any]
    priority: int = 1
    timestamp: Optional[float] = None
```

### Response Structure

```python
@dataclass
class AgentResponse:
    agent_name: str
    success: bool
    data: Any
    error_message: Optional[str] = None
    execution_time: float = 0.0
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Make your changes**: Follow the established coding patterns
4. **Add tests**: Include tests for new functionality
5. **Submit a pull request**: Provide clear description of changes

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- **Issues**: Create an issue in the repository
- **Documentation**: Check this README and inline code documentation
- **Community**: Join our community discussions

---

**Built with ❤️ for modern project management teams**

---

## 🧭 ADK-style Coordinator with LiteLLM

This repository includes a coordinator `src/core/google_agent_development_kit_coordinator.py` that uses LiteLLM to perform LLM tool-calling. The tools are backed by the existing MCP-based Jira and Confluence agents.

### Configure (.env)

⚠️ **IMPORTANT**: Before running the project, you must obtain API tokens and configure your environment.

1) Copy the example env file and fill values:

```bash
cp env.example .env
```

2) Edit `.env` and set your secrets and URLs. Environment variables are loaded automatically by the package.

### 🔑 Required Tokens and Setup

#### **1. LiteLLM Model Configuration**
Set up your AI model provider:

```bash
# For OpenAI-compatible API (like Rakuten internal API)
LITELLM_MODEL=openai/gpt-4o-mini
LITELLM_API_BASE=https://your-api-endpoint.com/openai/v1
LITELLM_API_KEY=your-api-key-here
OPENAI_API_KEY=your-api-key-here  # Fallback for LiteLLM
```

#### **2. Atlassian API Tokens**

##### **Jira & Confluence Setup:**

1. **Create Atlassian Account**: Go to [atlassian.com](https://atlassian.com) and create an account
2. **Generate API Token**:
   - Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
   - Click "Create API token"
   - Give it a label (e.g., "AI Scrum Master")
   - Copy the generated token

3. **Get Your Atlassian Host**: Your Atlassian domain (e.g., `yourcompany.atlassian.net`)

4. **Create Basic Auth Token**: Combine your email and API token:
   ```bash
   # Format: base64(email:api_token)
   echo -n "your-email@domain.com:ATATT3xFfGF0..." | base64
   ```

5. **Configure in .env**:
   ```bash
   # Atlassian URLs
   JIRA_MCP_URL=https://yourcompany.atlassian.net/rest/api/3
   CONFLUENCE_MCP_URL=https://yourcompany.atlassian.net/wiki/rest/api
   
   # Authentication (use the base64 string from step 4)
   JIRA_MCP_AUTH_TOKEN=Basic <base64-email:token>
   CONFLUENCE_MCP_AUTH_TOKEN=Basic <base64-email:token>
   ```

#### **3. SSL Configuration**
For development/testing with self-signed certificates:

```bash
# Set to "false" for development, "true" for production
MCP_VERIFY_SSL=false
```

### 📋 Complete .env Example

```bash
# LiteLLM / Model configuration
LITELLM_MODEL=openai/gpt-4o-mini
LITELLM_API_BASE=https://api.openai.com/v1
LITELLM_API_KEY=your-openai-api-key
OPENAI_API_KEY=your-openai-api-key

# Atlassian URLs
JIRA_MCP_URL=https://yourcompany.atlassian.net/rest/api/3
CONFLUENCE_MCP_URL=https://yourcompany.atlassian.net/wiki/rest/api

# Atlassian Authentication
JIRA_MCP_AUTH_TOKEN=Basic <base64-encoded-email:token>
CONFLUENCE_MCP_AUTH_TOKEN=Basic <base64-encoded-email:token>

# SSL verification (false for dev, true for production)
MCP_VERIFY_SSL=false
```

### 🚨 Security Notes

- **Never commit `.env` files**: The `.gitignore` excludes `.env` files automatically
- **Use environment-specific tokens**: Different tokens for dev/staging/production
- **Rotate tokens regularly**: Generate new API tokens periodically
- **Limit token permissions**: Only grant necessary permissions to API tokens

### Run the AI Scrum Master

After setting up your `.env` file with the required tokens:

```bash
export PYTHONPATH=.
python ai_scrum_master.py
```

The coordinator will either:
- translate free-form instructions into tool calls chosen by the LLM, or
- execute structured `Command`s directly against the tool backends.

### 📊 Enhanced Logging

The AI Scrum Master now includes comprehensive logging for all creation and update operations:

#### **What Gets Logged:**
- **🎫 Jira Issues**: Creation/update with full details (key, summary, assignee, priority, direct URLs)
- **📄 Confluence Pages**: Creation/update with full details (ID, title, space, version, direct URLs)
- **🤖 AI Processing**: Request processing, tool selection, and execution status
- **📊 Operation Summaries**: High-level summaries of what was created/updated

#### **Example Log Output:**
```
2025-08-11 16:30:05,771 - 🤖 AI Processing request: Create a Confluence page in space 'MFS'...
2025-08-11 16:30:05,771 - 🔧 AI selected 1 tool(s) to execute
2025-08-11 16:30:05,771 - 🛠️  Executing tool: confluence_create_page
2025-08-11 16:30:05,771 - 📄 Creating Confluence page in space 'MFS': Enhanced Logging Test
2025-08-11 16:30:06,779 - 🎯 Confluence Page Created Successfully:
2025-08-11 16:30:06,779 -    📌 ID: 65933
2025-08-11 16:30:06,779 -    📋 Title: Enhanced Logging Test
2025-08-11 16:30:06,779 -    🔗 URL: https://athonprompt.atlassian.net/wiki/spaces/MFS/pages/65933
2025-08-11 16:30:06,779 - 📊 CREATION SUMMARY - Confluence Page: Enhanced Logging Test (ID: 65933)
```

#### **Benefits:**
- **🔍 Full Traceability**: Track every creation and modification
- **🔗 Direct Access**: Click-ready URLs to all created content  
- **📈 Progress Monitoring**: Real-time feedback on AI operations
- **🐛 Easy Debugging**: Comprehensive error context and logs

### Agent initialization style

You can initialize agents using the requested style:

```python
from src.core.llm_agent import LlmAgent, LiteLlm

splunk_agent = LlmAgent(
    name="splunk_query_agent",
    model=LiteLlm(
        model="gpt-4.1-mini",
        api_base="https://api.ai.public.rakuten-it.com/openai/v1",
        api_key=os.getenv("LITELLM_API_KEY"),
    ),
)
```
