from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class WorkflowMode(str, Enum):
    AUTO = "auto"
    LIGHTWEIGHT = "lightweight"
    FULL = "full"

class AgentType(str, Enum):
    PLANNER = "planner"
    CODE_GENERATOR = "code_generator"
    DEBUG = "debug"
    TEST = "test"
    OPTIMIZATION = "optimization"
    EXPLANATION = "explanation"

class TaskRequest(BaseModel):
    prompt: str = Field(..., description="User's coding request")
    language: Optional[str] = Field("python", description="Programming language")
    context: Optional[str] = Field(None, description="Additional context")
    workflow_mode: Optional[WorkflowMode] = Field(WorkflowMode.AUTO, description="Workflow complexity mode")

class AgentTask(BaseModel):
    agent_type: AgentType
    task_description: str
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    status: TaskStatus = TaskStatus.PENDING
    error_message: Optional[str] = None
    execution_time: Optional[float] = None

class CodeExecutionResult(BaseModel):
    success: bool
    status: str = "Completed"
    output: str = ""
    compilation_output: Optional[str] = None
    runtime_output: Optional[str] = None
    error: Optional[str] = None
    execution_time: float

class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    generated_code: Optional[str] = None
    execution_result: Optional[CodeExecutionResult] = None
    explanation: Optional[str] = None
    optimization_suggestions: Optional[List[str]] = None
    test_results: Optional[List[Dict[str, Any]]] = None
    agent_tasks: List[AgentTask] = []
    created_at: datetime
    completed_at: Optional[datetime] = None

class AgentLog(BaseModel):
    task_id: Optional[str] = None
    agent_type: AgentType
    message: str
    timestamp: datetime
    level: str = "info"
