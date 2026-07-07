from typing import Dict, Any, List
from .base_agent import BaseAgent
from models.task_model import AgentTask, TaskStatus, AgentType
from services.code_runner import CodeRunner

class TestAgent(BaseAgent):
    def __init__(self, ai_service, code_runner: CodeRunner):
        super().__init__(ai_service, AgentType.TEST)
        self.code_runner = code_runner
    
    def process(self, task: AgentTask) -> AgentTask:
        """Generate and run tests for the code"""
        try:
            self._log_activity("Starting testing phase")
            
            # Get the code (could be original or fixed code from debug agent)
            code = task.input_data.get("fixed_code") or task.input_data.get("generated_code", "")
            language = task.input_data.get("language", "python")
            
            if not code:
                return self._update_task_status(
                    task, TaskStatus.FAILED,
                    error_message="No code provided for testing"
                )
            
            # Generate tests
            self._log_activity("Generating test cases")
            test_code = self.ai_service.generate_tests(code, language)
            
            # Run tests
            self._log_activity("Running generated tests")
            test_results = self.code_runner.run_tests(code, language)
            
            # Analyze test results
            test_analysis = self._analyze_test_results(test_results)
            
            output_data = {
                "test_code": test_code,
                "test_results": test_results,
                "test_analysis": test_analysis,
                "code_under_test": code
            }
            
            status = TaskStatus.COMPLETED if test_analysis["tests_passed"] else TaskStatus.FAILED
            
            self._log_activity(f"Testing completed - {'Passed' if test_analysis['tests_passed'] else 'Failed'}")
            
            return self._update_task_status(task, status, output_data)
            
        except Exception as e:
            self._log_activity(f"Testing failed: {str(e)}", "error")
            return self._update_task_status(task, TaskStatus.FAILED, error_message=str(e))
    
    def _analyze_test_results(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the test execution results"""
        test_result = test_results.get("test_result", {})
        
        analysis = {
            "tests_passed": test_result.get("success", False),
            "test_output": test_result.get("output", ""),
            "test_errors": test_result.get("error", ""),
            "execution_time": test_result.get("execution_time", 0),
            "test_count": self._count_tests(test_results.get("test_code", "")),
            "summary": ""
        }
        
        # Create summary
        if analysis["tests_passed"]:
            analysis["summary"] = f"All {analysis['test_count']} tests passed successfully"
        else:
            analysis["summary"] = f"Tests failed. Error: {analysis['test_errors']}"
        
        return analysis
    
    def _count_tests(self, test_code: str) -> int:
        """Count the number of test cases in the generated test code"""
        if not test_code:
            return 0
        
        # Simple counting based on common test patterns
        test_patterns = [
            "def test_",
            "test(",
            "it(",
            "describe(",
            "@Test",
            "unittest.TestCase",
            "pytest"
        ]
        
        count = 0
        for pattern in test_patterns:
            count += test_code.count(pattern)
        
        return max(count, 1)  # Return at least 1 if test code exists
