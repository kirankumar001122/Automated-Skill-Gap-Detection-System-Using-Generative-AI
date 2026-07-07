# Nexora AI Quick Start Guide

## Prerequisites
- Python 3.9+
- Node.js 18+
- Ollama (with at least one model installed)
- npm or yarn

## Setup Steps

### 1. Backend Setup

```bash
# Navigate to project directory
cd ProjectStu

# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt
```

### 2. Ollama Setup

```bash
# Install Ollama (if not already installed)
# Download from https://ollama.ai

# Start Ollama server
ollama serve

# In another terminal, pull a model
ollama pull codellama
# or
ollama pull deepseek-coder
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build if needed
npm run build
```

### 4. Start the Application

**Terminal 1 - Backend API:**
```bash
cd ProjectStu
# Activate venv
.venv\Scripts\activate  # Windows

# Start backend
python -m uvicorn backend.main:app --reload
# Backend running on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd ProjectStu/frontend

# Start development server
npm run dev
# Frontend running on http://localhost:3000
```

### 5. Access the Application

- **Main App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## Usage

1. **Select Language**: Choose your programming language from the dropdown
2. **Enter Prompt**: Describe what code you want to generate
3. **Generate**: Click "Generate Code" or press Ctrl+Enter
4. **Watch Progress**: See real-time agent execution in the console
5. **Review Code**: View generated code in the editor
6. **Run/Debug/Optimize**: Use action buttons to test and improve code

## Example Prompts

### Python
```
Write a function that takes a list of numbers and returns the sum of all even numbers
```

### Java
```
Create a class to represent a person with name and age, include a toString method
```

### JavaScript
```
Write a React component for a todo list with add and delete functionality
```

### C++
```
Implement a binary search function for a sorted array
```

### TypeScript
```
Create an interface for API response with generic type support
```

## Troubleshooting

### Backend connection error
- Ensure backend is running on http://localhost:8000
- Check firewall settings
- Verify CORS is enabled

### Ollama connection error
- Ensure Ollama server is running
- Default URL: http://localhost:11434
- Run: `ollama serve` in a separate terminal

### No models available
- List available models: `ollama list`
- Pull a model: `ollama pull codellama`

### Code execution errors
- Check language syntax
- Ensure required libraries are installed
- Review error message in console

## Configuration

### Backend Environment Variables
```
PORT=8000
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=codellama
LOG_LEVEL=INFO
```

### Frontend Environment Variables
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## File Structure

```
ProjectStu/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── routes/
│   │   └── agent_routes.py    # API endpoints
│   ├── agents/                 # 6 agent implementations
│   │   ├── agent_orchestrator.py
│   │   ├── planner_agent.py
│   │   ├── code_agent.py
│   │   ├── debug_agent.py
│   │   ├── test_agent.py
│   │   ├── optimizer_agent.py
│   │   └── explanation_agent.py
│   ├── services/
│   │   ├── ollama_service.py  # LLM integration
│   │   └── code_runner.py     # Code execution
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx           # Main dashboard
│   │   ├── components/         # React components
│   │   ├── services/           # API client
│   │   └── globals.css         # Tailwind styles
│   ├── package.json
│   └── next.config.js
│
└── SYSTEM_REDESIGN_COMPLETE.md
```

## API Endpoints

### POST /api/v1/generate-code
Generate code using the multi-agent system.

**Request:**
```json
{
  "prompt": "Write a factorial function",
  "language": "python",
  "context": ""
}
```

**Response:**
```json
{
  "task_id": "uuid",
  "status": "completed",
  "generated_code": "def factorial(n): ...",
  "agent_tasks": [...],
  "execution_result": {...},
  "explanation": "..."
}
```

### POST /api/v1/run-code
Execute code directly.

**Request:**
```json
{
  "code": "print('Hello')",
  "language": "python"
}
```

**Response:**
```json
{
  "success": true,
  "output": "Hello",
  "error": null,
  "execution_time": 0.123
}
```

### WS /ws/logs/{task_id}
WebSocket connection for real-time logs.

**Message Format:**
```json
{
  "agent": "planner",
  "message": "✓ Planner completed",
  "level": "info",
  "timestamp": "2026-05-14T10:30:45"
}
```

## Performance Tips

1. **Use CodeLlama**: Generally better for code generation
2. **GPU Acceleration**: Ensure Ollama can use GPU
3. **Batch Requests**: Limit concurrent requests
4. **Monitor Memory**: Watch memory usage for large code

## Support

For issues or questions:
1. Check error messages in backend console
2. Review system logs
3. Verify Ollama connectivity
4. Test with simpler prompts first

---

**Happy Coding! 🚀**
