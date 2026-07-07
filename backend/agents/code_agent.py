from typing import Dict, Any
from .base_agent import BaseAgent
from models.task_model import AgentTask, TaskStatus, AgentType

class CodeGeneratorAgent(BaseAgent):
    def __init__(self, ai_service):
        super().__init__(ai_service, AgentType.CODE_GENERATOR)
    
    def process(self, task: AgentTask) -> AgentTask:
        """Generate code based on the user request and plan"""
        try:
            self._log_activity("Starting code generation")
            
            # Extract input data
            prompt = task.input_data.get("prompt", "")
            language = task.input_data.get("language", "python")
            plan_steps = task.input_data.get("plan_steps", [])
            
            # Create enhanced prompt with plan context
            enhanced_prompt = self._create_enhanced_prompt(prompt, language, plan_steps)
            
            # Generate code using AI
            generated_code = self.ai_service.generate_code(enhanced_prompt, language)
            
            output_data = {
                "generated_code": generated_code,
                "language": language,
                "prompt": prompt
            }
            
            self._log_activity(f"Code generated successfully ({len(generated_code)} characters)")
            
            return self._update_task_status(task, TaskStatus.COMPLETED, output_data)
            
        except Exception as e:
            self._log_activity(f"Code generation failed: {str(e)}", "error")
            return self._update_task_status(task, TaskStatus.FAILED, error_message=str(e))
    
    def _create_enhanced_prompt(self, prompt: str, language: str, plan_steps: list) -> str:
        """Create an enhanced prompt that includes the planning context"""
        enhanced = f"""
        Generate {language} code for the following request:
        
        REQUEST: {prompt}
        
        IMPLEMENTATION PLAN:
        """
        
        for step in plan_steps:
            enhanced += f"\n{step.get('step_number', '')}. {step.get('title', '')}"
            if step.get('description'):
                enhanced += f"\n   {step['description']}"
        
        enhanced += f"""
        
        Guidelines:
        - Clean, efficient {language} code
        - Follow best practices and include error handling
        - Complete and runnable implementation
        
        Return ONLY the code. No explanations.
        """
        
        return enhanced
