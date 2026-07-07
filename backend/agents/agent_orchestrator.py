from typing import List, Dict, Any, Optional
import asyncio
import uuid
from datetime import datetime
import logging
from models.task_model import (
    TaskRequest, TaskResponse, AgentTask, AgentType, TaskStatus, AgentLog, WorkflowMode
)
from services.ai_service import AIService, AIConfig
from services.code_runner import CodeRunner
from .planner_agent import PlannerAgent
from .code_agent import CodeGeneratorAgent
from .debug_agent import DebugAgent
from .test_agent import TestAgent
from .optimizer_agent import OptimizationAgent
from .explanation_agent import ExplanationAgent

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    def __init__(self, ai_config: Optional[AIConfig] = None):
        self.ai_service = AIService(ai_config)
        self.code_runner = CodeRunner(self.ai_service)
        
        # Initialize all agents
        self.agents = {
            AgentType.PLANNER: PlannerAgent(self.ai_service),
            AgentType.CODE_GENERATOR: CodeGeneratorAgent(self.ai_service),
            AgentType.DEBUG: DebugAgent(self.ai_service, self.code_runner),
            AgentType.TEST: TestAgent(self.ai_service, self.code_runner),
            AgentType.OPTIMIZATION: OptimizationAgent(self.ai_service, self.code_runner),
            AgentType.EXPLANATION: ExplanationAgent(self.ai_service)
        }
        
        self.active_tasks: Dict[str, TaskResponse] = {}
        self.agent_logs: List[AgentLog] = []
        
        # Retry configuration
        self.max_retries = 2
        self.retry_delay = 2  # increased delay
        self.workflow_timeout = 180  # 180 seconds overall timeout
    
    async def process_request(self, request: TaskRequest) -> TaskResponse:
        """Process a user request through the multi-agent pipeline"""
        task_id = str(uuid.uuid4())
        created_at = datetime.now()
        
        # Create initial task response
        task_response = TaskResponse(
            task_id=task_id,
            status=TaskStatus.IN_PROGRESS,
            created_at=created_at,
            agent_tasks=[]
        )
        
        self.active_tasks[task_id] = task_response
        
        try:
            # Execute the entire workflow with a global timeout
            return await asyncio.wait_for(
                self._run_workflow_pipeline(task_id, request, task_response),
                timeout=self.workflow_timeout
            )
        except asyncio.TimeoutError:
            logger.error(f"Workflow Task {task_id} timed out after {self.workflow_timeout}s")
            task_response.status = TaskStatus.FAILED
            task_response.completed_at = datetime.now()
            error_msg = f"Workflow Timeout: Execution exceeded {self.workflow_timeout} seconds. The system was busy or the prompt was too complex."
            self._log_agent_activity(AgentType.PLANNER, f"✗ {error_msg}", "error", task_id)
            return task_response
        except Exception as e:
            logger.error(f"Task processing failed: {e}", exc_info=True)
            task_response.status = TaskStatus.FAILED
            task_response.completed_at = datetime.now()
            self._log_agent_activity(AgentType.PLANNER, f"✗ Workflow failed: {str(e)}", "error", task_id)
            return task_response

    async def _run_workflow_pipeline(self, task_id: str, request: TaskRequest, task_response: TaskResponse) -> TaskResponse:
        """Internal pipeline execution with dynamic complexity and parallelism"""
        
        # Determine workflow mode
        mode = request.workflow_mode
        if mode == WorkflowMode.AUTO:
            mode = self._detect_complexity(request.prompt)
            logger.info(f"Auto-detected workflow mode: {mode.value}")
        
        # Shared context for all agents
        shared_context = {
            "language": request.language,
            "prompt": request.prompt,
            "context": request.context
        }

        # Phase 1: Planning (Always required)
        await self._execute_agent_phase(task_id, AgentType.PLANNER, shared_context)
        planner_task = self._get_latest_agent_task(task_id, AgentType.PLANNER)
        if not planner_task or planner_task.status != TaskStatus.COMPLETED:
            raise Exception("Planning phase failed")
        
        # Phase 2: Generation (Always required)
        gen_input = {**shared_context, **planner_task.output_data}
        await self._execute_agent_phase(task_id, AgentType.CODE_GENERATOR, gen_input)
        gen_task = self._get_latest_agent_task(task_id, AgentType.CODE_GENERATOR)
        if not gen_task or gen_task.status != TaskStatus.COMPLETED:
            raise Exception("Generation phase failed")
            
        current_best_code_task = gen_task
        
        # Phase 3: Conditional Debugging
        if mode == WorkflowMode.FULL:
            debug_input = {**shared_context, **gen_task.output_data}
            await self._execute_agent_phase(task_id, AgentType.DEBUG, debug_input)
            debug_task = self._get_latest_agent_task(task_id, AgentType.DEBUG)
            if debug_task and debug_task.status == TaskStatus.COMPLETED:
                current_best_code_task = debug_task

        # Phase 4: Parallel Execution of TEST and OPTIMIZATION (Full mode only)
        if mode == WorkflowMode.FULL:
            para_input = {**shared_context, **current_best_code_task.output_data}
            
            # Run Test and Optimization in parallel
            self._log_agent_activity(AgentType.PLANNER, "🚀 Starting Parallel Testing and Optimization...", "info", task_id)
            await asyncio.gather(
                self._execute_agent_phase(task_id, AgentType.TEST, para_input),
                self._execute_agent_phase(task_id, AgentType.OPTIMIZATION, para_input)
            )
        
        # Phase 5: Explanation (Always required)
        # Get the final code from whichever agent finished last/best
        final_context = {**shared_context, **current_best_code_task.output_data}
        
        # Add test results or optimization suggestions if available
        opt_task = self._get_latest_agent_task(task_id, AgentType.OPTIMIZATION)
        if opt_task and opt_task.status == TaskStatus.COMPLETED:
            final_context.update(opt_task.output_data)
            
        test_task = self._get_latest_agent_task(task_id, AgentType.TEST)
        if test_task and test_task.status == TaskStatus.COMPLETED:
            final_context.update(test_task.output_data)

        await self._execute_agent_phase(task_id, AgentType.EXPLANATION, final_context)
        
        # Compile final results
        await self._compile_final_results(task_id)
        
        # Update task status
        task_response.status = TaskStatus.COMPLETED
        task_response.completed_at = datetime.now()
        
        self._log_agent_activity(AgentType.PLANNER, f"✓ Workflow ({mode.value}) completed successfully", "info", task_id)
        return task_response

    def _detect_complexity(self, prompt: str) -> WorkflowMode:
        """Detect if a prompt is simple enough for lightweight workflow"""
        prompt_lower = prompt.lower()
        simple_keywords = [
            "hello world", "factorial", "palindrome", "odd even", "fibonacci", 
            "sum of", "print", "basic", "simple", "checker"
        ]
        
        # If prompt is very short or contains simple keywords, use lightweight
        if len(prompt) < 100 or any(kw in prompt_lower for kw in simple_keywords):
            # Check if it's NOT a complex request disguised as simple
            complex_keywords = ["architecture", "framework", "database", "api", "integration", "full stack"]
            if not any(ck in prompt_lower for ck in complex_keywords):
                return WorkflowMode.LIGHTWEIGHT
                
        return WorkflowMode.FULL
    
    async def _execute_agent_phase(self, task_id: str, agent_type: AgentType, input_data: Dict[str, Any]):
        """Execute a single agent phase with retry logic"""
        agent = self.agents[agent_type]
        agent_display_name = agent_type.value.replace('_', ' ').title()
        
        for attempt in range(self.max_retries + 1):
            # Create agent task
            agent_task = AgentTask(
                agent_type=agent_type,
                task_description=f"Executing {agent_display_name} Phase",
                input_data=input_data,
                status=TaskStatus.PENDING,
                output_data={}
            )
            
            # Add to task response (or update if retry)
            if task_id in self.active_tasks:
                if attempt == 0:
                    self.active_tasks[task_id].agent_tasks.append(agent_task)
                else:
                    # Update the existing task
                    for i, task in enumerate(self.active_tasks[task_id].agent_tasks):
                        if task.agent_type == agent_type and task.status != TaskStatus.COMPLETED:
                            self.active_tasks[task_id].agent_tasks[i] = agent_task
                            break
            
            # Log agent start
            if attempt == 0:
                self._log_agent_activity(agent_type, f"⚙ {agent_display_name} starting...", "info", task_id)
            else:
                self._log_agent_activity(agent_type, f"🔄 {agent_display_name} retry {attempt}/{self.max_retries}...", "info", task_id)
            
            try:
                # Process the task
                start_time = datetime.now()
                updated_task = agent.process(agent_task)
                end_time = datetime.now()
                
                # Update execution time
                updated_task.execution_time = (end_time - start_time).total_seconds()
                
                # Update the task in the response
                if task_id in self.active_tasks:
                    task_response = self.active_tasks[task_id]
                    for i, task in enumerate(task_response.agent_tasks):
                        if task.agent_type == agent_type and task.status == TaskStatus.PENDING:
                            task_response.agent_tasks[i] = updated_task
                            break
                
                if updated_task.status == TaskStatus.COMPLETED:
                    execution_time_ms = updated_task.execution_time * 1000
                    self._log_agent_activity(
                        agent_type, 
                        f"✓ {agent_display_name} completed successfully ({execution_time_ms:.1f}ms)",
                        "info",
                        task_id
                    )
                    return  # Success, no need to retry
                else:
                    # Task failed but not an exception - check if we should retry
                    error_msg = updated_task.error_message or "Unknown error"
                    if attempt < self.max_retries:
                        self._log_agent_activity(
                            agent_type,
                            f"⚠ {agent_display_name} attempt {attempt + 1} failed: {error_msg}, retrying...",
                            "warning",
                            task_id
                        )
                        await asyncio.sleep(self.retry_delay)
                        continue
                    else:
                        self._log_agent_activity(
                            agent_type,
                            f"✗ {agent_display_name} failed after {self.max_retries + 1} attempts: {error_msg}",
                            "error",
                            task_id
                        )
                        return
                
            except Exception as e:
                error_msg = str(e)
                if attempt < self.max_retries:
                    self._log_agent_activity(
                        agent_type,
                        f"⚠ {agent_display_name} error on attempt {attempt + 1}: {error_msg}, retrying...",
                        "warning",
                        task_id
                    )
                    await asyncio.sleep(self.retry_delay)
                    continue
                else:
                    logger.error(f"Agent {agent_type.value} execution failed after {self.max_retries + 1} attempts: {e}", exc_info=True)
                    agent_task.status = TaskStatus.FAILED
                    agent_task.error_message = f"Failed after {self.max_retries + 1} attempts: {error_msg}"
                    self._log_agent_activity(
                        agent_type,
                        f"✗ {agent_display_name} error: {agent_task.error_message}",
                        "error",
                        task_id
                    )
                    return
    
    def _get_latest_agent_task(self, task_id: str, agent_type: AgentType) -> Optional[AgentTask]:
        """Get the latest task for a specific agent"""
        if task_id not in self.active_tasks:
            return None
        
        tasks = [task for task in self.active_tasks[task_id].agent_tasks 
                if task.agent_type == agent_type]
        return tasks[-1] if tasks else None
    
    def _get_previous_agent_output(self, task_id: str, current_agent: AgentType) -> Optional[Dict[str, Any]]:
        """Get output data from previous agents to use as context"""
        if task_id not in self.active_tasks:
            return None
        
        task_response = self.active_tasks[task_id]
        agent_order = [
            AgentType.PLANNER,
            AgentType.CODE_GENERATOR,
            AgentType.DEBUG,
            AgentType.TEST,
            AgentType.OPTIMIZATION,
            AgentType.EXPLANATION
        ]
        
        current_index = agent_order.index(current_agent)
        previous_agents = agent_order[:current_index]
        
        context = {}
        for agent_type in reversed(previous_agents):
            agent_task = self._get_latest_agent_task(task_id, agent_type)
            if agent_task and agent_task.status == TaskStatus.COMPLETED and agent_task.output_data:
                context.update(agent_task.output_data)
                break
        
        return context
    
    async def _compile_final_results(self, task_id: str):
        """Compile final results from all agent phases"""
        if task_id not in self.active_tasks:
            return
        
        task_response = self.active_tasks[task_id]
        
        # Get results from each agent
        code_task = self._get_latest_agent_task(task_id, AgentType.CODE_GENERATOR)
        debug_task = self._get_latest_agent_task(task_id, AgentType.DEBUG)
        test_task = self._get_latest_agent_task(task_id, AgentType.TEST)
        optimization_task = self._get_latest_agent_task(task_id, AgentType.OPTIMIZATION)
        explanation_task = self._get_latest_agent_task(task_id, AgentType.EXPLANATION)
        
        # Set final code (prefer optimized version)
        if optimization_task and optimization_task.output_data:
            task_response.generated_code = optimization_task.output_data.get("final_code")
            task_response.optimization_suggestions = optimization_task.output_data.get("optimization_suggestions", [])
        elif debug_task and debug_task.output_data:
            task_response.generated_code = debug_task.output_data.get("fixed_code")
        elif code_task and code_task.output_data:
            task_response.generated_code = code_task.output_data.get("generated_code")
        
        # Set execution result
        if debug_task and debug_task.output_data:
            execution_result = debug_task.output_data.get("execution_result")
            if execution_result:
                from models.task_model import CodeExecutionResult
                task_response.execution_result = CodeExecutionResult(**execution_result)
        
        # Set test results
        if test_task and test_task.output_data:
            test_analysis = test_task.output_data.get("test_analysis")
            if test_analysis:
                task_response.test_results = [test_analysis]
        
        # Set explanation
        if explanation_task and explanation_task.output_data:
            task_response.explanation = explanation_task.output_data.get("explanation")
    
    def _log_agent_activity(self, agent_type: AgentType, message: str, level: str = "info", task_id: Optional[str] = None):
        """Log agent activity"""
        log_entry = AgentLog(
            task_id=task_id,
            agent_type=agent_type,
            message=message,
            timestamp=datetime.now(),
            level=level
        )
        self.agent_logs.append(log_entry)
        
        # Keep only last 200 logs to support more history
        if len(self.agent_logs) > 200:
            self.agent_logs = self.agent_logs[-200:]
    
    def get_task_status(self, task_id: str) -> Optional[TaskResponse]:
        """Get the current status of a task"""
        return self.active_tasks.get(task_id)
    
    def get_agent_logs(self, task_id: Optional[str] = None, limit: int = 50) -> List[AgentLog]:
        """Get agent logs, optionally filtered by task"""
        if task_id:
            # Filter logs for specific task
            relevant_logs = [log for log in self.agent_logs if log.task_id == task_id or log.task_id is None]
            return relevant_logs[-limit:]
        return self.agent_logs[-limit:]
