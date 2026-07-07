from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
import uvicorn
import os
import json
import asyncio
from datetime import datetime
from routes.agent_routes import router as agent_router
from services.ai_service import AIService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Nexora AI API",
    description="🤖 Premium AI-powered autonomous coding workspace and multi-agent system",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS (Allow frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(agent_router)

# WebSocket clients tracking
connected_clients: dict[str, list[WebSocket]] = {}

@app.websocket("/ws/logs/{task_id}")
async def websocket_logs(websocket: WebSocket, task_id: str):
    """WebSocket endpoint for real-time agent logs"""
    await websocket.accept()
    
    # Track this client
    if task_id not in connected_clients:
        connected_clients[task_id] = []
    connected_clients[task_id].append(websocket)
    
    logger.info(f"Client connected to task {task_id}")
    
    try:
        # Keep connection alive and send logs
        last_log_count = 0
        while True:
            # Check for new logs every 100ms
            from routes.agent_routes import orchestrator
            logs = orchestrator.get_agent_logs(task_id, limit=100)
            
            if len(logs) > last_log_count:
                # Send only new logs
                for log in logs[last_log_count:]:
                    log_data = {
                        "agent": log.agent_type.value,
                        "message": log.message,
                        "level": log.level,
                        "timestamp": log.timestamp.isoformat()
                    }
                    await websocket.send_json(log_data)
                    last_log_count += 1
            
            # Small delay to avoid busy-waiting
            await asyncio.sleep(0.1)
            
    except WebSocketDisconnect:
        logger.info(f"Client disconnected from task {task_id}")
        connected_clients[task_id].remove(websocket)
    except Exception as e:
        logger.error(f"WebSocket error for task {task_id}: {e}")
        if task_id in connected_clients and websocket in connected_clients[task_id]:
            connected_clients[task_id].remove(websocket)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Autonomous Coding Agent API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/api/v1/health",
        "websocket": "/ws/logs/{task_id}"
    }

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    try:
        ai_service = AIService()
        models = ai_service.list_models()
        return {
            "status": "healthy",
            "provider": "OpenAI",
            "models": models,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.warning(f"Health check warning: {e}")
        return {
            "status": "degraded",
            "message": "AI Service connection check failed",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/health")
async def health_check_root():
    """Health check endpoint for browser access"""
    return {"status": "healthy", "service": "autonomous-coding-agent"}

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("=" * 60)
    logger.info("🚀 Nexora AI: Autonomous Coding Workspace Starting")
    logger.info("=" * 60)
    
    # Test AI connection
    try:
        ai_service = AIService()
        if ai_service.config.api_key:
            logger.info("✔ AI API Key loaded successfully")
        else:
            logger.warning("⚠ AI API Key is missing in .env")
            
        models = ai_service.list_models()
        logger.info(f"✓ AI Service connected. Available models: {', '.join(models)}")
    except Exception as e:
        logger.error(f"✗ Failed to connect to AI Service: {e}")
        logger.info("Please ensure OPENROUTER_API_KEY or OPENAI_API_KEY is set in .env")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Shutting down Autonomous Coding Agent...")

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    host = "0.0.0.0"  # Allow external access
    
    logger.info(f"\n📡 Backend API running on http://localhost:{port}")
    logger.info(f"📚 API Docs: http://localhost:{port}/docs")
    logger.info(f"🔌 WebSocket: ws://localhost:{port}/ws/logs/{{task_id}}")
    logger.info(f"🌐 Frontend: http://localhost:3000\n")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info",
        timeout_keep_alive=180,
       
    )
