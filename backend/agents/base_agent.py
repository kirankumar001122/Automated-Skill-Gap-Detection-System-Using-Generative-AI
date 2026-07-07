from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from models.task_model import AgentTask, AgentType, TaskStatus
from services.ai_service import AIService

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self, ai_service: AIService, agent_type: AgentType):
        self.ai_service = ai_service
        self.agent_type = agent_type
    
    @abstractmethod
    def process(self, task: AgentTask) -> AgentTask:
        """Process the assigned task and return updated task with results"""
        pass
    
    def _log_activity(self, message: str, level: str = "info"):
        logger.log(
            logging.INFO if level == "info" else logging.ERROR,
            f"[{self.agent_type.value}] {message}"
        )
    
    def _update_task_status(self, task: AgentTask, status: TaskStatus, 
                           output_data: Optional[Dict[str, Any]] = None,
                           error_message: Optional[str] = None) -> AgentTask:
        task.status = status
        if output_data:
            task.output_data = output_data
        if error_message:
            task.error_message = error_message
        return task
