from typing import Dict, Any
from .base_agent import BaseAgent
from models.task_model import AgentTask, TaskStatus, AgentType

class ExplanationAgent(BaseAgent):
    def __init__(self, ai_service):
        super().__init__(ai_service, AgentType.EXPLANATION)
    
    def process(self, task: AgentTask) -> AgentTask:
        """Provide clear explanation of the final code"""
        try:
            self._log_activity("Starting explanation phase")
            
            # Get the final code (could be optimized or original)
            final_code = task.input_data.get("final_code") or \
                         task.input_data.get("optimized_code") or \
                         task.input_data.get("fixed_code") or \
                         task.input_data.get("generated_code", "")
            
            language = task.input_data.get("language", "python")
            original_prompt = task.input_data.get("prompt", "")
            
            # Get additional context from other agents if available
            optimization_suggestions = task.input_data.get("optimization_suggestions", [])
            test_results = task.input_data.get("test_results", {})
            
            if not final_code:
                return self._update_task_status(
                    task, TaskStatus.FAILED,
                    error_message="No code available for explanation"
                )
            
            # Generate comprehensive explanation
            explanation = self._generate_comprehensive_explanation(
                final_code, language, original_prompt, optimization_suggestions, test_results
            )
            
            # Generate code summary
            code_summary = self._generate_code_summary(final_code, language)
            
            # Generate usage examples
            usage_examples = self._generate_usage_examples(final_code, language, original_prompt)
            
            output_data = {
                "explanation": explanation,
                "code_summary": code_summary,
                "usage_examples": usage_examples,
                "language": language,
                "complexity_analysis": self._analyze_complexity(final_code),
                "key_features": self._extract_key_features(final_code)
            }
            
            self._log_activity("Code explanation completed successfully")
            
            return self._update_task_status(task, TaskStatus.COMPLETED, output_data)
            
        except Exception as e:
            self._log_activity(f"Explanation failed: {str(e)}", "error")
            return self._update_task_status(task, TaskStatus.FAILED, error_message=str(e))
    
    def _generate_comprehensive_explanation(self, code: str, language: str, 
                                           original_prompt: str, optimization_suggestions: list,
                                           test_results: dict) -> str:
        """Generate a comprehensive explanation of the code"""
        return self.ai_service.explain_code(code, language)
    
    def _generate_code_summary(self, code: str, language: str) -> str:
        """Generate a brief summary of the code"""
        system_prompt = f"""Provide a concise 2-3 sentence summary of what this {language} code does.
        Be specific about the functionality and purpose. Do not explain implementation details."""
        
        return self.ai_service.generate_response(code, system_prompt)
    
    def _generate_usage_examples(self, code: str, language: str, original_prompt: str) -> str:
        """Generate practical usage examples"""
        system_prompt = f"""Generate 2-3 practical usage examples for this {language} code.
        Include sample input/output where applicable. Be concise and directly usable."""
        
        prompt = f"Code that does: {original_prompt}\n\nCode:\n{code}\n\nProvide usage examples."
        
        return self.ai_service.generate_response(prompt, system_prompt)
    
    def _analyze_complexity(self, code: str) -> Dict[str, Any]:
        """Analyze code complexity"""
        lines = len(code.split('\n'))
        functions = code.count('def ') + code.count('function ') + code.count('function(')
        classes = code.count('class ') + code.count('class {')
        
        # Simple complexity estimation
        if lines < 20:
            complexity = "Simple"
        elif lines < 50:
            complexity = "Moderate"
        elif lines < 100:
            complexity = "Complex"
        else:
            complexity = "Very Complex"
        
        return {
            "lines_of_code": lines,
            "functions": functions,
            "classes": classes,
            "complexity_level": complexity
        }
    
    def _extract_key_features(self, code: str) -> list:
        """Extract key features from the code"""
        features = []
        
        # Look for common patterns
        if "import " in code:
            features.append("Uses external libraries/modules")
        
        if "try:" in code or "except" in code:
            features.append("Includes error handling")
        
        if "def " in code or "function " in code:
            features.append("Modular function-based design")
        
        if "class " in code:
            features.append("Object-oriented programming")
        
        if "input(" in code or "argv" in code:
            features.append("Accepts user input")
        
        if "print(" in code or "console.log" in code:
            features.append("Produces output")
        
        if "for " in code or "while " in code:
            features.append("Uses loops/iteration")
        
        if "if " in code or "switch" in code:
            features.append("Conditional logic")
        
        return features if features else ["Basic code structure"]
