#!/usr/bin/env python3
"""
Demo script showing how users interact with the Scrum Master agent
through the Google Agent Development Kit web interface.

This demonstrates the user-driven approach where users provide
their own Jira project keys and Confluence space keys.
"""
import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.scrum_master_coordinator import ScrumMasterCoordinator


async def demo_user_interactions():
    """Demonstrate user-driven Scrum Master interactions."""
    print("🏃‍♂️ AI Scrum Master Demo - User-Driven Project Management")
    print("=" * 65)
    
    # Initialize Scrum Master
    coordinator = ScrumMasterCoordinator()
    await coordinator.initialize()
    
    # Demo conversations showing how users will interact
    conversations = [
        {
            "title": "🚀 Starting a New Sprint",
            "messages": [
                "Hi! I want to start a new sprint for my team. Can you help me?",
                "I want to start Sprint 7 with the goal of implementing user dashboard features. My Jira project is 'DASH' and Confluence space is 'TEAM'."
            ]
        },
        {
            "title": "📋 Sprint Planning Session", 
            "messages": [
                "Can you help me plan our current sprint? I need to assign tasks to my team members.",
                """I want to plan a sprint in Jira project 'DASH'. Here are the requirements:
                
Requirements:
- User Profile Management (High priority, 16 hours, needs React and API skills)
- Dashboard Analytics (Medium priority, 12 hours, needs Data Analysis and Python)
- Notification System (High priority, 20 hours, needs WebSocket and Node.js)

Team Members:
- alice.dev (React, JavaScript, API) - 80% capacity
- bob.data (Python, Data Analysis, SQL) - 90% capacity  
- charlie.backend (Node.js, WebSocket, API) - 75% capacity"""
            ]
        },
        {
            "title": "🗣️ Daily Standup",
            "messages": [
                "Can you run our daily standup for project 'DASH'? I want to see the current status."
            ]
        },
        {
            "title": "📊 Sprint Burndown",
            "messages": [
                "Show me the burndown chart for our current sprint in project 'DASH'."
            ]
        }
    ]
    
    for i, conversation in enumerate(conversations, 1):
        print(f"\n{i}. {conversation['title']}")
        print("-" * 60)
        
        for j, message in enumerate(conversation['messages'], 1):
            print(f"\n👤 User Message {j}:")
            print(f"   {message}")
            print(f"\n🤖 Scrum Master Response:")
            
            try:
                responses = await coordinator.chat_execute(message)
                for response in responses:
                    if response.success:
                        print(f"   ✅ {response.data}")
                    else:
                        print(f"   ❌ {response.error_message}")
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
            
            print()
    
    print("=" * 65)
    print("🎯 Demo Complete!")
    print("\n💡 Key Features Demonstrated:")
    print("• ✅ User provides their own Jira project keys")
    print("• ✅ User specifies their Confluence space keys") 
    print("• ✅ Dynamic project configuration")
    print("• ✅ Real-time sprint management")
    print("• ✅ Intelligent task assignment")
    print("• ✅ Team capacity planning")
    print("• ✅ Progress tracking and reporting")
    
    print("\n🌐 To use with Google Agent Development Kit web interface:")
    print("1. Run: adk web")
    print("2. Access the web interface") 
    print("3. Chat with the Scrum Master")
    print("4. Provide your Jira project key and Confluence space when prompted")
    
    await coordinator.shutdown()


def print_usage_guide():
    """Print usage guide for the Scrum Master."""
    print("""
🏃‍♂️ AI Scrum Master Usage Guide
================================

The AI Scrum Master helps you manage your agile projects through natural conversation.
You'll need to provide your specific Jira and Confluence information.

📋 What You'll Need:
• Jira Project Key (e.g., 'PROJ', 'DEV', 'TEAM') 
• Confluence Space Key (e.g., 'DEV', 'DOCS', 'TEAM')
• Team member information (names, skills, capacity)
• Sprint requirements and goals

🎯 What the Scrum Master Can Do:
• Start new sprints with documentation
• Plan sprints with intelligent task assignment  
• Conduct daily standups with progress reports
• Generate burndown charts and metrics
• Assign tasks based on team member skills
• Track team capacity and workload
• Create Confluence documentation automatically

💬 Example Conversations:
• "Help me start Sprint 5 for project ABC in space DEV"
• "Plan a sprint with these requirements for project XYZ" 
• "Run a standup for project TEAM"
• "Show burndown chart for project DASH"
• "Assign these tasks to my team in project PROD"

🌐 Access Methods:
• Google Agent Development Kit: adk web
• REST API: /api/v1/projects/execute
• Direct Python: ScrumMasterCoordinator.chat_execute()

🔗 Integration Ready:
• Works with existing Jira instances
• Integrates with Confluence spaces
• Supports any project structure
• Adapts to your team's workflow
""")


if __name__ == "__main__":
    print_usage_guide()
    print("\n" + "="*65)
    asyncio.run(demo_user_interactions())
