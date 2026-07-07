# Nexora AI Installation Guide

## 🚀 Quick Start

Get Nexora AI up and running on your machine:

### Prerequisites Checklist

Before you begin, ensure you have:

- [ ] **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
  - Download from [docker.com](https://docker.com)
  - Verify with: `docker --version`

- [ ] **Ollama** installed locally
  - Install with: `curl -fsSL https://ollama.ai/install.sh | sh`
  - Verify with: `ollama --version`

- [ ] **8GB+ RAM** available
  - Check with: `free -h` (Linux) or Task Manager (Windows)

- [ ] **20GB+ free disk space**

---

## 📦 Step-by-Step Installation

### Step 1: Install Ollama and Models

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull coding models (choose one or more)
ollama pull codellama:7b          # Good for general coding
ollama pull deepseek-coder:6.7b   # Excellent for code
ollama pull llama3:8b             # General purpose

# Verify models are installed
ollama list
```

### Step 2: Clone the Project

```bash
# Clone the repository
git clone <repository-url>
cd autonomous-coding-agent

# Copy environment configuration
cp .env.example .env
```

### Step 3: Start the Application

#### Option A: Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build

# Check if everything is running
docker-compose ps
```

#### Option B: Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Step 4: Verify Installation

Open your browser and navigate to:

- **Application**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

You should see the Autonomous Coding Agent interface!

---

## 🧪 Test Your Installation

Try these example prompts:

1. **Simple Python Function**:
   ```
   Create a function that calculates the factorial of a number
   ```

2. **REST API**:
   ```
   Build a simple Flask REST API with endpoints for GET and POST users
   ```

3. **Data Processing**:
   ```
   Write a script to read a CSV file and calculate basic statistics
   ```

---

## 🔧 Common Installation Issues

### Issue: "Ollama connection failed"

**Solution:**
```bash
# Check if Ollama is running
ollama serve

# Test connection
curl http://localhost:11434/api/tags

# If it fails, restart Ollama
pkill ollama
ollama serve
```

### Issue: "Docker build fails"

**Solution:**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check Docker daemon is running
docker info
```

### Issue: "Port already in use"

**Solution:**
```bash
# Find what's using the port
netstat -tulpn | grep :8000
netstat -tulpn | grep :3000

# Kill the process or change ports in .env
```

### Issue: "Out of memory"

**Solution:**
```bash
# Check available memory
free -h

# Increase Docker memory allocation in Docker Desktop settings
# Or use smaller Ollama models
ollama pull codellama:3b
```

---

## 🎯 Next Steps

Once installed:

1. **Explore the Interface**: Try different prompts and languages
2. **Check Agent Activity**: Monitor how agents work together
3. **Review Generated Code**: Use the explanation feature
4. **Run Tests**: Verify code quality with the test agent
5. **Optimize**: Improve performance with the optimization agent

---

## 📚 Additional Resources

- [User Guide](README.md) - Complete usage documentation
- [API Documentation](docs/api.md) - API reference
- [Troubleshooting](docs/troubleshooting.md) - Common issues
- [Configuration Guide](docs/configuration.md) - Advanced setup

---

## 💡 Tips for Best Performance

1. **Use SSD Storage**: Faster I/O for better performance
2. **Allocate More RAM**: Give Docker Desktop at least 4GB
3. **Choose Right Model**: `codellama:7b` for balance, `deepseek-coder` for code
4. **Monitor Resources**: Use `docker stats` to check usage
5. **Regular Updates**: Keep Ollama models updated

---

## 🆘 Getting Help

If you're still having trouble:

1. **Check the logs**: `docker-compose logs -f`
2. **Verify prerequisites**: Run the checklist above
3. **Search issues**: Check GitHub Issues
4. **Join community**: Ask in discussions

---

**Happy coding! 🚀**
