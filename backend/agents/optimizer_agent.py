from typing import Dict, Any, List
from .base_agent import BaseAgent
from models.task_model import AgentTask, TaskStatus, AgentType
from services.code_runner import CodeRunner

class OptimizationAgent(BaseAgent):
    def __init__(self, ai_service, code_runner: CodeRunner):
        super().__init__(ai_service, AgentType.OPTIMIZATION)
        self.code_runner = code_runner
    
    def process(self, task: AgentTask) -> AgentTask:
        """Optimize the code for performance and readability"""
        try:
            self._log_activity("Starting optimization phase")
            
            # Get the best version of code (prefer fixed code over original)
            code = task.input_data.get("fixed_code") or task.input_data.get("generated_code", "")
            language = task.input_data.get("language", "python")
            
            if not code:
                return self._update_task_status(
                    task, TaskStatus.FAILED,
                    error_message="No code provided for optimization"
                )
            
            # Get baseline performance
            baseline_result = self.code_runner.run_code(code, language)
            
            # Optimize the code
            self._log_activity("Generating optimized code")
            optimized_code = self.ai_service.optimize_code(code, language)
            
            # Test optimized code
            optimized_result = self.code_runner.run_code(optimized_code, language)
            
            # Compare performance
            performance_comparison = self._compare_performance(
                baseline_result, optimized_result
            )
            
            # Generate optimization suggestions
            suggestions = self._generate_optimization_suggestions(
                code, optimized_code, performance_comparison
            )
            
            # Determine which code is better
            final_code = optimized_code if self._is_optimization_better(
                baseline_result, optimized_result
            ) else code
            
            output_data = {
                "original_code": code,
                "optimized_code": optimized_code,
                "final_code": final_code,
                "baseline_performance": baseline_result,
                "optimized_performance": optimized_result,
                "performance_comparison": performance_comparison,
                "optimization_suggestions": suggestions,
                "optimization_applied": final_code == optimized_code
            }
            
            self._log_activity(f"Optimization completed - {'Applied' if final_code == optimized_code else 'Kept original'}")
            
            return self._update_task_status(task, TaskStatus.COMPLETED, output_data)
            
        except Exception as e:
            self._log_activity(f"Optimization failed: {str(e)}", "error")
            return self._update_task_status(task, TaskStatus.FAILED, error_message=str(e))
    
    def _compare_performance(self, baseline: Dict[str, Any], optimized: Dict[str, Any]) -> Dict[str, Any]:
        """Compare performance between baseline and optimized versions"""
        comparison = {
            "baseline_success": baseline.get("success", False),
            "optimized_success": optimized.get("success", False),
            "baseline_time": baseline.get("execution_time", 0),
            "optimized_time": optimized.get("execution_time", 0),
            "time_improvement": 0,
            "performance_improved": False,
            "both_successful": baseline.get("success", False) and optimized.get("success", False)
        }
        
        if comparison["both_successful"]:
            time_diff = comparison["baseline_time"] - comparison["optimized_time"]
            comparison["time_improvement"] = time_diff
            comparison["performance_improved"] = time_diff > 0.01  # At least 10ms improvement
        
        return comparison
    
    def _generate_optimization_suggestions(self, original: str, optimized: str, 
                                         comparison: Dict[str, Any]) -> List[str]:
        """Generate optimization suggestions based on the changes made"""
        suggestions = []
        
        # Performance-based suggestions
        if comparison["performance_improved"]:
            improvement_ms = comparison["time_improvement"] * 1000
            suggestions.append(f"Performance improved by {improvement_ms:.2f}ms")
        elif comparison["both_successful"] and not comparison["performance_improved"]:
            suggestions.append("Performance maintained with improved readability")
        
        # Code quality suggestions
        if len(optimized) != len(original):
            if len(optimized) < len(original):
                suggestions.append("Code made more concise")
            else:
                suggestions.append("Code expanded for better clarity")
        
        # Success-based suggestions
        if not comparison["baseline_success"] and comparison["optimized_success"]:
            suggestions.append("Fixed functionality issues")
        elif comparison["baseline_success"] and not comparison["optimized_success"]:
            suggestions.append("Optimization broke functionality - using original")
        
        # Add generic suggestions if none were generated
        if not suggestions:
            suggestions.append("Code reviewed for best practices")
            suggestions.append("Consider further optimization based on specific use case")
        
        return suggestions
    
    def _is_optimization_better(self, baseline: Dict[str, Any], optimized: Dict[str, Any]) -> bool:
        """Determine if the optimized version is better than baseline"""
        baseline_success = baseline.get("success", False)
        optimized_success = optimized.get("success", False)
        
        # If optimization breaks functionality, keep original
        if baseline_success and not optimized_success:
            return False
        
        # If optimization fixes broken functionality, use it
        if not baseline_success and optimized_success:
            return True
        
        # If both work, consider performance
        if baseline_success and optimized_success:
            baseline_time = baseline.get("execution_time", 0)
            optimized_time = optimized.get("execution_time", 0)
            # Use optimized if it's faster or at least not significantly slower
            return optimized_time <= baseline_time * 1.1  # Allow 10% slowdown for readability
        
        # If both fail, keep original (less risk)
        return False
