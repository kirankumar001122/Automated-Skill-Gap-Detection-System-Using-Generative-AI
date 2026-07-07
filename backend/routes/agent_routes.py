from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional, List
import logging
from models.task_model import TaskRequest, TaskResponse
from agents.agent_orchestrator import AgentOrchestrator
from services.ai_service import AIConfig

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["agents"])

from pydantic import BaseModel

# Global orchestrator instance
orchestrator = AgentOrchestrator()

class RunCodeRequest(BaseModel):
    code: str
    language: str = "python"
    input_data: Optional[str] = None

class CodeActionRequest(BaseModel):
    code: str
    language: str = "python"

@router.post("/generate-code", response_model=TaskResponse)
async def generate_code(request: TaskRequest):
    """Generate code using the multi-agent system"""
    try:
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        if not request.language:
            request.language = "python"
        
        # Validate language
        valid_languages = ["python", "java", "c", "cpp", "c++", "javascript", "typescript"]
        if request.language.lower() not in valid_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language: {request.language}. Supported: {', '.join(valid_languages)}"
            )
        
        logger.info(f"Code generation request: language={request.language}, prompt={request.prompt[:100]}...")
        
        # Process the request
        task_response = await orchestrator.process_request(request)
        
        logger.info(f"Task {task_response.task_id} completed with status {task_response.status}")
        return task_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Code generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Code generation failed: {str(e)}")

@router.post("/debug-code")
async def debug_code(request: CodeActionRequest):
    """Debug and fix code issues"""
    try:
        from models.task_model import TaskRequest
        task_req = TaskRequest(
            prompt=f"Debug and fix this {request.language} code. Identify bugs and provide a corrected version.",
            language=request.language,
            context=request.code
        )
        
        task_response = await orchestrator.process_request(task_req)
        return task_response
        
    except Exception as e:
        logger.error(f"Debug failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/run-code")
async def run_code(request: RunCodeRequest):
    """Execute code locally"""
    try:
        if not request.code.strip():
            raise HTTPException(status_code=400, detail="Code cannot be empty")
        
        valid_languages = ["python", "java", "c", "cpp", "c++", "javascript", "typescript"]
        if request.language.lower() not in valid_languages:
            raise HTTPException(status_code=400, detail=f"Unsupported language: {request.language}")
        
        logger.info(f"Running code in {request.language}")
        
        from services.code_runner import CodeRunner
        from services.ai_service import AIService
        
        ai_service = AIService()
        code_runner = CodeRunner(ai_service)
        
        result = code_runner.run_code(request.code, request.language, request.input_data)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Code execution failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")

@router.post("/optimize-code")
async def optimize_code(request: CodeActionRequest):
    """Optimize code for performance and readability"""
    try:
        from models.task_model import TaskRequest
        task_req = TaskRequest(
            prompt=f"Perform a comprehensive code quality analysis on this {request.language} code. 1) Detect syntax/logical errors. 2) Suggest code optimizations. 3) Highlight potential bugs. 4) Recommend best practices. Provide the optimized version and your analysis.",
            language=request.language,
            context=request.code
        )
        
        task_response = await orchestrator.process_request(task_req)
        return task_response
        
    except Exception as e:
        logger.error(f"Optimization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/explain-code")
async def explain_code(request: CodeActionRequest):
    """Get explanation of code"""
    try:
        from models.task_model import TaskRequest
        task_req = TaskRequest(
            prompt=f"Provide a step-by-step explanation of this {request.language} code in very simple language. Carefully explain the core logic, functions, loops, and expected outputs.",
            language=request.language,
            context=request.code
        )
        
        task_response = await orchestrator.process_request(task_req)
        return task_response
        
    except Exception as e:
        logger.error(f"Explanation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/task/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: str):
    """Get the status of a specific task"""
    task_response = orchestrator.get_task_status(task_id)
    
    if not task_response:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task_response

@router.get("/logs")
async def get_agent_logs(task_id: Optional[str] = None, limit: int = 50):
    """Get agent activity logs"""
    logs = orchestrator.get_agent_logs(task_id, limit)
    return {"logs": logs}

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "autonomous-coding-agent"}

@router.get("/models")
async def get_available_models():
    """Get available AI models"""
    try:
        models = orchestrator.ai_service.list_models()
        return {"models": models}
    except Exception as e:
        logger.error(f"Failed to get models: {e}")
        return {"models": [], "error": str(e)}
