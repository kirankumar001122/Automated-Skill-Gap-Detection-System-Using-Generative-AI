import json
import re
from datetime import datetime
from typing import Dict, Any, List
from .base_agent import BaseAgent
from models.task_model import AgentTask, AgentType, TaskStatus

class PlannerAgent(BaseAgent):
    def __init__(self, ai_service):
        super().__init__(ai_service, AgentType.PLANNER)
    
    def process(self, task: AgentTask) -> AgentTask:
        """Create an execution plan for the user request"""
        try:
            self._log_activity("Starting planning phase")
            
            # Extract user request from input data
            user_request = task.input_data.get("prompt", "")
            language = task.input_data.get("language", "python")
            context = task.input_data.get("context", "")
            
            # Create comprehensive prompt for planning
            planning_prompt = self._create_planning_prompt(user_request, language, context)
            
            # Generate plan using AI
            plan = self.ai_service.create_plan(planning_prompt, language)
            
            # Parse plan into structured steps
            steps = self._parse_plan(plan)
            
            # Create subtasks for other agents
            subtasks = self._create_subtasks(steps, language, user_request)
            
            output_data = {
                "plan": plan,
                "steps": steps,
                "subtasks": subtasks,
                "language": language
            }
            
            self._log_activity(f"Plan created with {len(steps)} steps and {len(subtasks)} subtasks")
            
            return self._update_task_status(task, TaskStatus.COMPLETED, output_data)
            
        except Exception as e:
            self._log_activity(f"Planning failed: {str(e)}", "error")
            return self._update_task_status(task, TaskStatus.FAILED, error_message=str(e))
    
    def _create_planning_prompt(self, user_request: str, language: str, context: str) -> str:
        """Create a concise prompt for the planning phase"""
        return f"""
        User Request: {user_request}
        Language: {language}
        Context: {context if context else "None"}
        
        Provide a concise implementation plan (max 5-7 steps).
        Each step should include a title and short description.
        """
    
    def _parse_plan(self, plan: str) -> List[Dict[str, Any]]:
        """Parse the generated plan into structured steps"""
        if not plan:
            return [{"step_number": 1, "title": "Implementation", "description": "Implement the requested functionality.", "deliverable": "Working code"}]

        steps = []
        # Support both numbered lists and bullet points
        lines = plan.split('\n')
        current_step = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Match patterns like "1. Title", "Step 1: Title", "- Title"
            step_match = re.match(r'^(?:Step\s+)?(\d+)[\.:\)]\s*(.*)', line, re.IGNORECASE)
            
            if step_match:
                if current_step:
                    steps.append(current_step)
                
                step_num = step_match.group(1)
                step_title = step_match.group(2).strip()
                current_step = {
                    "step_number": int(step_num),
                    "title": step_title or f"Step {step_num}",
                    "description": "",
                    "deliverable": ""
                }
            elif current_step:
                # Add to current step description
                if ":" in line and any(keyword in line.lower() for keyword in ["output", "deliverable", "result"]):
                    current_step["deliverable"] = line.split(":", 1)[1].strip()
                else:
                    current_step["description"] = (current_step["description"] + " " + line).strip()
        
        if current_step:
            steps.append(current_step)
        
        # If no steps found, create a default one
        if not steps:
            steps.append({
                "step_number": 1,
                "title": "Implementation",
                "description": plan[:200] + "..." if len(plan) > 200 else plan,
                "deliverable": "Source code"
            })
            
        return steps
    
    def _create_subtasks(self, steps: List[Dict[str, Any]], language: str, user_request: str) -> List[Dict[str, Any]]:
        """Create subtasks for other agents based on the plan"""
        subtasks = []
        
        # Always start with code generation
        subtasks.append({
            "agent_type": AgentType.CODE_GENERATOR,
            "description": "Generate initial code implementation",
            "priority": 1,
            "input_data": {
                "prompt": user_request,
                "language": language,
                "plan_steps": steps
            }
        })
        
        # Add debugging task
        subtasks.append({
            "agent_type": AgentType.DEBUG,
            "description": "Debug and fix any issues in generated code",
            "priority": 2,
            "input_data": {
                "language": language
            }
        })
        
        # Add testing task
        subtasks.append({
            "agent_type": AgentType.TEST,
            "description": "Generate and run comprehensive tests",
            "priority": 3,
            "input_data": {
                "language": language
            }
        })
        
        # Add optimization task
        subtasks.append({
            "agent_type": AgentType.OPTIMIZATION,
            "description": "Optimize code for performance and readability",
            "priority": 4,
            "input_data": {
                "language": language
            }
        })
        
        # Add explanation task
        subtasks.append({
            "agent_type": AgentType.EXPLANATION,
            "description": "Provide clear explanation of the final code",
            "priority": 5,
            "input_data": {
                "language": language
            }
        })
        
        return subtasks
