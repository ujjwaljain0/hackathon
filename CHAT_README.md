# 🤖 AI Scrum Master Chat Interface

A beautiful, interactive chat interface to interact directly with the AI Scrum Master agent.

## 🚀 **Quick Start**

1. **Start the API server:**
   ```bash
   python3 run_api_server.py
   ```

2. **Open the chat interface:**
   - **URL:** http://localhost:8000/chat
   - **API Docs:** http://localhost:8000/docs

## 💬 **How to Use**

### **Web Interface (Recommended)**
- Open http://localhost:8000/chat in your browser
- Type your questions about Scrum, sprint planning, or team coordination
- Get instant AI-powered responses and guidance

### **API Endpoint**
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Help me plan a 2-week sprint"}'
```

## 🎯 **What You Can Ask**

### **Sprint Planning**
- "Help me plan a 2-week sprint for a new feature"
- "How many story points should I plan for a 2-week sprint?"
- "What should I include in sprint planning?"

### **Task Breakdown**
- "Help me break down a complex feature into smaller tasks"
- "How do I estimate story points for user stories?"
- "What's the best way to organize tasks in a sprint?"

### **Team Coordination**
- "How do I run an effective daily standup?"
- "What should I include in a sprint retrospective?"
- "How do I handle team capacity planning?"

### **Scrum Best Practices**
- "What are the key Scrum ceremonies?"
- "How do I write good user stories?"
- "What's the difference between velocity and capacity?"

## ✨ **Features**

- **🎨 Beautiful UI:** Modern, responsive design with smooth animations
- **💬 Real-time Chat:** Instant responses from AI Scrum Master
- **📱 Mobile Friendly:** Works perfectly on all devices
- **🔗 Session Management:** Maintains conversation context
- **📝 Smart Formatting:** Supports markdown-like formatting
- **⚡ Fast Responses:** Async processing for quick replies

## 🛠️ **Technical Details**

- **Frontend:** Pure HTML/CSS/JavaScript (no frameworks)
- **Backend:** FastAPI with async processing
- **AI Integration:** LiteLLM with OpenAI GPT models
- **Real-time:** WebSocket-like experience with typing indicators

## 🔧 **Customization**

### **Styling**
- Edit `chat_interface.html` to customize colors, fonts, and layout
- Modify CSS variables for easy theming
- Add custom animations and transitions

### **Functionality**
- Extend the chat with additional features
- Add file upload capabilities
- Integrate with external tools

## 📱 **Mobile Experience**

The chat interface is fully responsive and optimized for:
- 📱 Smartphones
- 📱 Tablets  
- 💻 Desktop computers
- 🖥️ Large monitors

## 🚨 **Troubleshooting**

### **Server Not Starting**
```bash
# Check if port 8000 is available
lsof -i :8000

# Kill any existing processes
pkill -f "python.*run_api_server.py"

# Start fresh
python3 run_api_server.py
```

### **Chat Not Working**
- Ensure the API server is running
- Check browser console for errors
- Verify the `/api/v1/chat` endpoint is accessible

### **Slow Responses**
- Check your internet connection
- Verify API key configuration
- Monitor server logs for errors

## 🌟 **Example Conversations**

### **Sprint Planning**
```
User: "I need to plan a 2-week sprint for a mobile app feature"
Bot: "Great! Let me help you plan that sprint. I'll need some details:
1. What's the main goal of this feature?
2. How many developers are available?
3. What's the current team velocity?
4. Any dependencies or constraints?"
```

### **Task Breakdown**
```
User: "Help me break down 'Implement user authentication'"
Bot: "Here's how I'd break down user authentication:
1. Set up authentication service (2-3 days)
2. Create login/register forms (1-2 days)
3. Implement JWT token handling (2 days)
4. Add password reset functionality (1-2 days)
5. Write tests and documentation (1-2 days)
Total: 7-11 days depending on complexity"
```

## 🎉 **Ready to Chat!**

Your AI Scrum Master is ready to help! Open http://localhost:8000/chat and start planning your next sprint with AI assistance.

---

**Built with ❤️ for agile teams who want intelligent Scrum guidance at their fingertips!**
