import docker
import tempfile
import os
import uuid
import time
from typing import Dict, Any, Optional, Tuple
import logging
from models.task_model import CodeExecutionResult

logger = logging.getLogger(__name__)

class DockerExecutor:
    def __init__(self):
        self.client = docker.from_env()
        self.timeout = 5  # seconds
        self.memory_limit = "128m"
        self.cpu_limit = 0.5
    
    def _create_temp_file(self, code: str, extension: str) -> str:
        temp_dir = tempfile.mkdtemp()
        filename = f"code_{uuid.uuid4().hex[:8]}.{extension}"
        filepath = os.path.join(temp_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        
        return filepath, temp_dir
    
    def _get_docker_image(self, language: str) -> str:
        language_images = {
            "python": "python:3.10-slim",
            "javascript": "node:18-slim",
            "java": "openjdk:17-slim",
            "cpp": "gcc:latest",
            "c": "gcc:latest"
        }
        return language_images.get(language.lower(), "python:3.10-slim")
    
    def _get_run_command(self, language: str, filepath: str) -> str:
        if language.lower() == "python":
            return f"python {os.path.basename(filepath)}"
        elif language.lower() == "javascript":
            return f"node {os.path.basename(filepath)}"
        elif language.lower() == "java":
            filename = os.path.basename(filepath).replace('.java', '')
            return f"javac {os.path.basename(filepath)} && java {filename}"
        elif language.lower() in ["cpp", "c"]:
            filename = os.path.basename(filepath).replace('.cpp', '').replace('.c', '')
            ext = '.cpp' if language.lower() == 'cpp' else '.c'
            return f"g++ -o {filename} {os.path.basename(filepath)} && ./{filename}"
        else:
            return f"python {os.path.basename(filepath)}"
    
    def execute_code(self, code: str, language: str = "python") -> CodeExecutionResult:
        start_time = time.time()
        
        try:
            # Create temporary file
            extension = self._get_file_extension(language)
            filepath, temp_dir = self._create_temp_file(code, extension)
            
            # Get Docker image and run command
            image = self._get_docker_image(language)
            run_command = self._get_run_command(language, filepath)
            
            # Pull image if not available
            try:
                self.client.images.get(image)
            except docker.errors.ImageNotFound:
                logger.info(f"Pulling Docker image: {image}")
                self.client.images.pull(image)
            
            # Create and run container
            container = self.client.containers.create(
                image=image,
                command=run_command,
                volumes={temp_dir: {'bind': '/app', 'mode': 'rw'}},
                working_dir='/app',
                mem_limit=self.memory_limit,
                cpu_quota=int(self.cpu_limit * 100000),
                network_mode='none',  # Disable network access
                remove=True
            )
            
            # Start container and wait for completion
            container.start()
            
            # Wait for container to finish or timeout
            exit_code = container.wait(timeout=self.timeout)
            
            # Get logs
            stdout = container.logs(stdout=True, stderr=False).decode('utf-8')
            stderr = container.logs(stdout=False, stderr=True).decode('utf-8')
            
            execution_time = time.time() - start_time
            
            # Clean up
            container.remove(force=True)
            os.remove(filepath)
            os.rmdir(temp_dir)
            
            success = exit_code['StatusCode'] == 0
            
            return CodeExecutionResult(
                success=success,
                output=stdout if success else stderr,
                error=stderr if not success else None,
                execution_time=execution_time
            )
            
        except docker.errors.ContainerError as e:
            execution_time = time.time() - start_time
            return CodeExecutionResult(
                success=False,
                output="",
                error=str(e),
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Code execution failed: {e}")
            return CodeExecutionResult(
                success=False,
                output="",
                error=f"Execution error: {str(e)}",
                execution_time=execution_time
            )
    
    def _get_file_extension(self, language: str) -> str:
        extensions = {
            "python": "py",
            "javascript": "js",
            "java": "java",
            "cpp": "cpp",
            "c": "c"
        }
        return extensions.get(language.lower(), "py")
    
    def test_code(self, code: str, test_code: str, language: str = "python") -> Dict[str, Any]:
        try:
            # Combine code and tests
            if language.lower() == "python":
                combined_code = f"{code}\n\n{test_code}"
            else:
                combined_code = f"{code}\n{test_code}"
            
            result = self.execute_code(combined_code, language)
            
            return {
                "success": result.success,
                "output": result.output,
                "error": result.error,
                "execution_time": result.execution_time
            }
            
        except Exception as e:
            logger.error(f"Test execution failed: {e}")
            return {
                "success": False,
                "output": "",
                "error": f"Test execution error: {str(e)}",
                "execution_time": 0
            }
