from typing import Dict, Any, Optional
import logging
from .local_executor import LocalExecutor
from .ai_service import AIService

logger = logging.getLogger(__name__)

class CodeRunner:
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
        self.local_executor = LocalExecutor()
    
    def run_code(self, code: str, language: str = "python", input_data: Optional[str] = None) -> Dict[str, Any]:
        """Execute code and return results"""
        try:
            # Detect if code needs an execution block
            needs_exec = False
            code_lower = code.lower()
            if language == "python":
                needs_exec = not ("print(" in code_lower or "if __name__" in code_lower or "import unittest" in code_lower)
            elif language == "java":
                needs_exec = "public static void main" not in code_lower
            elif language in ["c", "cpp", "c++"]:
                needs_exec = "int main" not in code_lower
            elif language == "javascript":
                needs_exec = not ("console.log" in code_lower)
                
            if needs_exec:
                logger.info(f"Code lacks execution block. Generating execution block for {language}...")
                code = self.ai_service.augment_with_execution(code, language)

            result = self.local_executor.execute_code(code, language, input_data)
            return {
                "success": result.success,
                "status": result.status,
                "output": result.output,
                "compilation_output": result.compilation_output,
                "runtime_output": result.runtime_output,
                "error": result.error,
                "execution_time": result.execution_time
            }
        except Exception as e:
            logger.error(f"Code execution failed: {e}")
            return {
                "success": False,
                "status": "Failed",
                "output": "",
                "compilation_output": None,
                "runtime_output": None,
                "error": f"Execution failed: {str(e)}",
                "execution_time": 0
            }
    
    def run_tests(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Generate and run tests for the code"""
        try:
            # Generate tests
            test_code = self.ai_service.generate_tests(code, language)
            
            # Run tests
            test_result = self.local_executor.test_code(code, test_code, language)
            
            return {
                "test_code": test_code,
                "test_result": test_result
            }
        except Exception as e:
            logger.error(f"Test execution failed: {e}")
            return {
                "test_code": "",
                "test_result": {
                    "success": False,
                    "output": "",
                    "error": f"Test generation failed: {str(e)}",
                    "execution_time": 0
                }
            }
