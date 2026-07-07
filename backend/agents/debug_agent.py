from typing import Dict, Any
from .base_agent import BaseAgent
from models.task_model import AgentTask, TaskStatus, AgentType
from services.code_runner import CodeRunner

class DebugAgent(BaseAgent):
    def __init__(self, ai_service, code_runner: CodeRunner):
        super().__init__(ai_service, AgentType.DEBUG)
        self.code_runner = code_runner
    
    def process(self, task: AgentTask) -> AgentTask:
        """Debug and fix issues in the generated code"""
        try:
            self._log_activity("Starting debugging phase")
            
            # Get the code from previous agent's output
            # This would typically come from the code generator agent
            generated_code = task.input_data.get("generated_code", "")
            language = task.input_data.get("language", "python")
            
            if not generated_code:
                return self._update_task_status(
                    task, TaskStatus.FAILED, 
                    error_message="No code provided for debugging"
                )
            
            # First, try to run the code to identify issues
            execution_result = self.code_runner.run_code(generated_code, language)
            
            if execution_result["success"]:
                self._log_activity("Code runs without errors")
                output_data = {
                    "fixed_code": generated_code,
                    "issues_found": [],
                    "execution_result": execution_result
                }
                return self._update_task_status(task, TaskStatus.COMPLETED, output_data)
            
            # If there are errors, try to fix them
            error_message = execution_result.get("error", "Unknown error")
            self._log_activity(f"Found error: {error_message}")
            
            # Use AI to debug and fix the code
            fixed_code = self.ai_service.debug_code(generated_code, error_message, language)
            
            # Test the fixed code
            fixed_execution_result = self.code_runner.run_code(fixed_code, language)
            
            issues_found = [error_message] if error_message else []
            
            if fixed_execution_result["success"]:
                self._log_activity("Code successfully fixed")
                issues_found.append("Fixed successfully")
            else:
                self._log_activity("Code still has issues after attempted fix", "error")
                issues_found.append(f"Still failing: {fixed_execution_result.get('error', 'Unknown error')}")
            
            output_data = {
                "fixed_code": fixed_code,
                "original_code": generated_code,
                "issues_found": issues_found,
                "execution_result": fixed_execution_result,
                "original_execution_result": execution_result
            }
            
            status = TaskStatus.COMPLETED if fixed_execution_result["success"] else TaskStatus.FAILED
            
            return self._update_task_status(task, status, output_data)
            
        except Exception as e:
            self._log_activity(f"Debugging failed: {str(e)}", "error")
            return self._update_task_status(task, TaskStatus.FAILED, error_message=str(e))
