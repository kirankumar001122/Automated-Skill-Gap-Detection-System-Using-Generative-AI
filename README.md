# Nexora AI
## AI Autonomous Coding Workspace

A world-class, production-level AI-powered multi-agent system for automated software engineering. Nexora AI uses multiple specialized AI agents working together to understand user instructions, generate code, debug it, test it, and optimize it.

---

## ⚡ Quick Start (2 Options)

### 🏠 **Local Setup (No Docker) - RECOMMENDED for Development**

Get started in 5 minutes without Docker:

```bash
# 1. Make sure Ollama is running
ollama serve

# 2. Run the startup script (in another terminal)
cd C:\Users\YourUsername\Desktop\Kiran_documents\ProjectStu
.\run_local.bat
```

✅ **Pros**: Faster, easier debugging, no Docker Desktop needed  
📖 **Setup Guide**: [README_LOCAL.md](README_LOCAL.md)  
📚 **Detailed Guide**: [LOCAL_SETUP_GUIDE.md](LOCAL_SETUP_GUIDE.md)  

---

### 🐳 **Docker Setup - Production Ready**

For containerized deployment:

```bash
docker-compose up --build
```

✅ **Pros**: Isolated environments, production-ready, consistent across machines  
📖 **Setup Guide**: [Docker Setup Instructions](#docker-setup)

---

## 🚀 Features

- **Multi-Agent Architecture**: 6 specialized agents working in coordination
  - Planner Agent: Breaks down tasks into actionable steps
  - Code Generator Agent: Writes clean, efficient code
  - Debug Agent: Detects and fixes errors automatically
  - Test Agent: Generates and runs comprehensive tests
  - Optimization Agent: Improves performance and readability
  - Explanation Agent: Provides clear code explanations

- **Secure Code Execution**: Local subprocess or Docker-based sandbox
- **Multiple Language Support**: Python, JavaScript, Java, C++, C
- **Modern UI**: React-based interface with Monaco editor
- **Local LLM Integration**: Uses Ollama for privacy and control
- **Real-time Agent Monitoring**: Track agent activities and progress

---

## 📋 System Requirements

### For Local Setup (Recommended)

- **Python 3.10+**
- **Node.js 18+** (optional for JavaScript execution)
- **Ollama** (for LLM)
- **4GB+ RAM**
- **5GB disk space**

### For Docker Setup

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Node.js 18+** and npm
- **Python 3.10+**
- **Ollama** installed locally
- **8GB+ RAM**
- **20GB disk space**

---

## 🛠️ Installation Guide

### For Local Setup (Recommended)

**Simple 3-step setup:**

```bash
# Step 1: Install dependencies (one-time)
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..

# Step 2: Make sure Ollama is running
ollama serve  # Keep this running in background

# Step 3: Start the project
.\run_local.bat  # Windows
# OR
./run_local.sh   # Mac/Linux
```

**Then open:** http://localhost:3000

📖 **Full setup guide**: [LOCAL_SETUP_GUIDE.md](LOCAL_SETUP_GUIDE.md)  
📖 **Migration details**: [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)

---

### For Docker Setup

#### Step 1: Install Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull recommended models (this may take a while)
ollama pull codellama
ollama pull deepseek-coder
ollama pull llama3

# Verify installation
ollama list
```

#### Step 2: Docker Compose Setup

```bash
# Clone the repository
git clone <repository-url>
cd autonomous-coding-agent

# Build and start all services
docker-compose up --build

# Or start in detached mode
docker-compose up -d --build

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

#### Step 3: Environment Configuration

Create `.env` file in the project root:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=codellama

# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
PYTHONPATH=/app/backend

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Docker Configuration
COMPOSE_PROJECT_NAME=autonomous-coding-agent
```

---

## 🌐 Accessing the Application

Once running, access the application at:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

---

## 📖 Usage Guide

### Basic Code Generation

1. **Enter Your Request**: Type what you want to create in the prompt input
   - Example: "Create a function that calculates factorial"
   - Example: "Build a REST API for user management"

2. **Select Language**: Choose your preferred programming language

3. **Generate Code**: Click "Generate Code" or press Ctrl+Enter

4. **Review Results**: 
   - Generated code appears in the editor
   - Execution output shows in the console
   - Agent activity is displayed on the right

### Advanced Features

#### Debug Code
- Click "Debug Code" to automatically detect and fix errors
- The debug agent analyzes the code and provides fixes

#### Run Code
- Click "Run Code" to execute the current code
- Results appear in the output console

#### Optimize Code
- Click "Optimize Code" to improve performance and readability
- Optimization suggestions are provided

#### Explain Code
- Click "Explain Code" to get detailed explanations
- Learn what the code does and how it works

## 🔧 Configuration

### Ollama Models

The system works best with coding-focused models:

```bash
# Install recommended models
ollama pull codellama:7b
ollama pull deepseek-coder:6.7b
ollama pull llama3:8b

# Set default model in .env
OLLAMA_MODEL=codellama:7b
```

### Docker Configuration

For production deployments, modify `docker-compose.yml`:

```yaml
# Increase resource limits
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2.0'
```

### Security Settings

**Local Setup**: Code execution with same privileges as the Python process (suitable for development).

**Docker Setup**: Enhanced security features including:
- Code execution in isolated Docker containers
- Network restrictions for sandboxed code
- Execution time limits (5-10 seconds default)
- Memory and CPU limits per container

---

## 🐛 Troubleshooting

### For Local Setup

See detailed troubleshooting in [LOCAL_SETUP_GUIDE.md](LOCAL_SETUP_GUIDE.md#-troubleshooting)

**Quick Fixes:**
```bash
# Ollama not running
ollama serve

# Port already in use
netstat -ano | findstr :8000

# Module not found
pip install -r backend/requirements.txt

# Dependencies installation failed
pip install --upgrade -r backend/requirements.txt
```

### For Docker Setup

#### Ollama Connection Failed
```bash
# Check if Ollama is running
ollama serve

# Test connection
curl http://localhost:11434/api/tags

# Restart Ollama if needed
docker restart autonomous-coding-agent-ollama
```

#### Docker Build Failures
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

#### Frontend Not Loading
```bash
# Check backend health
curl http://localhost:8000/api/v1/health

# Restart services
docker-compose restart frontend backend
```

#### Code Execution Errors
```bash
# Check Docker daemon status
docker info

# Verify Docker socket permissions
ls -la /var/run/docker.sock
```

### Performance Optimization

#### For Better Performance (Local)
1. Use SSD storage
2. Close unnecessary applications
3. Increase available RAM
4. Use faster Ollama models (smaller size)

#### For Better Performance (Docker)
1. Use SSD storage
2. Allocate more RAM to Docker Desktop
3. Use GPU-accelerated Ollama if available
4. Increase worker processes in production

#### Memory Issues
1. Reduce Ollama model size (7B instead of 13B)
2. Limit concurrent requests
3. Increase system swap space
4. Use lighter Docker images (for Docker setup)

---

## 📚 API Documentation

### Endpoints

#### Generate Code
```http
POST /api/v1/generate-code
Content-Type: application/json

{
  "prompt": "Create a calculator function",
  "language": "python",
  "context": "optional additional context"
}
```

#### Run Code
```http
POST /api/v1/run-code
Content-Type: application/json

{
  "code": "print('Hello World')",
  "language": "python"
}
```

#### Debug Code
```http
POST /api/v1/debug-code
Content-Type: application/json

{
  "code": "buggy code here",
  "language": "python"
}
```

#### Get Task Status
```http
GET /api/v1/task/{task_id}
```

#### Get Agent Logs
```http
GET /api/v1/logs?limit=50
```

### Response Format

```json
{
  "task_id": "uuid-string",
  "status": "completed",
  "generated_code": "generated code here",
  "execution_result": {
    "success": true,
    "output": "execution output",
    "execution_time": 0.123
  },
  "explanation": "code explanation",
  "agent_tasks": [...]
}
```

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
   ```bash
   cp .env.example .env.production
   # Edit .env.production with production values
   ```

2. **Scale Services**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

3. **SSL Configuration**
   - Configure nginx with SSL certificates
   - Update environment variables for HTTPS

4. **Monitoring**
   - Set up log aggregation
   - Configure health checks
   - Monitor resource usage

### Cloud Deployment

The application can be deployed on:
- AWS (ECS/EKS)
- Google Cloud (GKE)
- Azure (AKS)
- DigitalOcean

See `deployment/` directory for cloud-specific configurations.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt
npm install --dev

# Run tests
pytest
npm test

# Code formatting
black .
prettier --write .
```

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and `/docs` folder
- **Issues**: Open an issue on GitHub
- **Discussions**: Join our GitHub Discussions
- **Community**: Join our Discord server

## 🎯 Roadmap

- [ ] Support for more programming languages
- [ ] Code completion and suggestions
- [ ] Project templates and scaffolding
- [ ] Git integration and version control
- [ ] Collaborative coding features
- [ ] Performance profiling
- [ ] Code review automation
- [ ] Multi-file project support
- [ ] Plugin system for custom agents

## 🙏 Acknowledgments

- Ollama for local LLM capabilities
- LangChain for agent orchestration
- FastAPI for the backend framework
- Next.js and React for the frontend
- Monaco Editor for code editing
- Docker for containerization

---

**Happy Coding! 🚀**
