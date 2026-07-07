import subprocess
import tempfile
import os
import uuid
import time
import sys
import re
from typing import Dict, Any, Optional, Tuple, List
import logging
from models.task_model import CodeExecutionResult

logger = logging.getLogger(__name__)

class LocalExecutor:
    """Execute code locally using subprocess (replaces Docker)"""
    
    def __init__(self):
        self.timeout = 30  # seconds
        self.temp_dir = tempfile.gettempdir()
        self._verify_java_runtime()

    def _verify_java_runtime(self):
        """Verify if Java and Javac are available in the system PATH"""
        logger.info("Verifying Java runtime...")
        self.java_installed = self._is_cmd_working(["java", "-version"])
        self.javac_installed = self._is_cmd_working(["javac", "-version"])
        
        if self.java_installed:
            logger.info("✔ Java is installed and working")
        else:
            logger.warning("✖ Java is NOT detected in PATH")
            
        if self.javac_installed:
            logger.info("✔ Javac is installed and working")
        else:
            logger.warning("✖ Javac is NOT detected in PATH")

    def _is_cmd_working(self, cmd_list: list) -> bool:
        """Verify if a command works using subprocess"""
        try:
            result = subprocess.run(
                cmd_list,
                capture_output=True,
                text=True,
                timeout=5
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
        except Exception as e:
            logger.debug(f"Error checking command {cmd_list}: {e}")
            return False

    def _extract_java_class_name(self, code: str) -> str:
        """Extract the public class name from Java code"""
        import re
        match = re.search(r'public\s+class\s+(\w+)', code)
        if match:
            return match.group(1)
        match = re.search(r'class\s+(\w+)', code)
        if match:
            return match.group(1)
        return "Main"

    def _create_temp_file(self, code: str, extension: str, language: str = "") -> Tuple[str, str]:
        """Create a temporary file with the code"""
        code = re.sub(r'```(?:\w+)?\s*', '', code)
        code = code.replace('```', '')
        
        temp_dir = tempfile.mkdtemp()
        
        if language.lower() == "java":
            class_name = self._extract_java_class_name(code)
            filename = f"{class_name}.java"
        else:
            filename = f"code_{uuid.uuid4().hex[:8]}.{extension}"
            
        filepath = os.path.join(temp_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code.strip())
        
        return filepath, temp_dir

    def _get_commands(self, language: str, filepath: str) -> Tuple[Optional[List[str]], List[str]]:
        """Get compile and run commands based on language"""
        language_lower = language.lower()
        dir_path = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        exe_name = filename.split('.')[0] + (".exe" if sys.platform == "win32" else "")
        exe_path = os.path.join(dir_path, exe_name)
        
        if language_lower == "python":
            return None, [sys.executable, filepath]
            
        elif language_lower == "javascript" or language_lower == "typescript":
            if self._check_command_available("node"):
                return None, ["node", filepath]
            else:
                raise Exception("Node.js is not installed.")
                
        elif language_lower == "java":
            class_name = filename.replace('.java', '')
            if self.javac_installed and self.java_installed:
                compile_cmd = ["javac", filepath]
                run_cmd = ["java", "-cp", dir_path, class_name]
                return compile_cmd, run_cmd
            else:
                raise Exception("JDK is not installed or not in PATH.")
                
        elif language_lower in ["cpp", "c++"]:
            if self._check_command_available("g++"):
                compile_cmd = ["g++", "-o", exe_path, filepath]
                run_cmd = [exe_path]
                return compile_cmd, run_cmd
            else:
                raise Exception("G++ is not installed.")
                
        elif language_lower == "c":
            if self._check_command_available("gcc"):
                compile_cmd = ["gcc", "-o", exe_path, filepath]
                run_cmd = [exe_path]
                return compile_cmd, run_cmd
            else:
                raise Exception("GCC is not installed.")
                
        else:
            return None, [sys.executable, filepath]

    def _check_command_available(self, command: str) -> bool:
        """Check if a command is available and working"""
        if not command:
            return False
        try:
            if os.path.isabs(command):
                return os.path.exists(command)
            cmd_where = "where" if sys.platform == "win32" else "which"
            result = subprocess.run(
                f"{cmd_where} {command}",
                shell=True,
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False

    def _kill_process_tree(self, pid: int):
        """Kill a process and all its children to prevent zombie processes."""
        try:
            import psutil
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            for child in children:
                child.kill()
            parent.kill()
        except ImportError:
            # Fallback for Windows if psutil is not available
            if sys.platform == "win32":
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(pid)], capture_output=True)
            else:
                try:
                    os.killpg(os.getpgid(pid), 9)
                except Exception:
                    pass
        except Exception as e:
            logger.warning(f"Error killing process tree for PID {pid}: {e}")

    def execute_code(self, code: str, language: str = "python", input_data: Optional[str] = None) -> CodeExecutionResult:
        """Execute code locally and return results"""
        start_time = time.time()
        
        compilation_output = ""
        runtime_output = ""
        error_msg = None
        status = "Completed"
        success = False
        
        try:
            extension = self._get_file_extension(language)
            filepath, temp_dir = self._create_temp_file(code, extension, language)
            
            compile_cmd, run_cmd = self._get_commands(language, filepath)
            
            # 1. Compilation Phase
            if compile_cmd:
                status = "Compiling"
                logger.info(f"Compiling {language}: {' '.join(compile_cmd)}")
                
                try:
                    comp_proc = subprocess.run(
                        compile_cmd, capture_output=True, text=True, timeout=15, cwd=os.path.dirname(filepath)
                    )
                    compilation_output = comp_proc.stdout
                    if comp_proc.stderr:
                        compilation_output += ("\n" if compilation_output else "") + comp_proc.stderr
                    
                    if comp_proc.returncode != 0:
                        status = "Failed"
                        error_msg = f"Compilation Error:\n{compilation_output}"
                        return CodeExecutionResult(
                            success=False,
                            status=status,
                            output=error_msg,
                            compilation_output=compilation_output.strip() if compilation_output else None,
                            runtime_output=None,
                            error=error_msg,
                            execution_time=round(time.time() - start_time, 2)
                        )
                except subprocess.TimeoutExpired:
                    status = "Failed"
                    return CodeExecutionResult(
                        success=False,
                        status=status,
                        output="Compilation timeout (took longer than 15s)",
                        compilation_output="Compilation timeout",
                        runtime_output=None,
                        error="Compilation timeout",
                        execution_time=round(time.time() - start_time, 2)
                    )
            
            # 2. Execution Phase
            status = "Executing"
            logger.info(f"Executing: {' '.join(run_cmd)}")
            
            try:
                creationflags = 0
                if sys.platform == "win32":
                    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
                
                proc = subprocess.Popen(
                    run_cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=os.path.dirname(filepath),
                    creationflags=creationflags
                )
                
                try:
                    stdout, stderr = proc.communicate(input=input_data or "", timeout=self.timeout)
                    runtime_output = stdout
                    
                    if proc.returncode == 0:
                        success = True
                        status = "Completed"
                        if stderr:
                            runtime_output += "\n[Warnings/Logs]:\n" + stderr
                    else:
                        success = False
                        status = "Failed"
                        error_msg = stderr or "Unknown Runtime Error"
                        if runtime_output:
                            error_msg = f"{error_msg}\nStdout:\n{runtime_output}"
                        
                except subprocess.TimeoutExpired:
                    self._kill_process_tree(proc.pid)
                    success = False
                    status = "Failed"
                    error_msg = f"Execution timeout. Code took longer than {self.timeout} seconds."
                    runtime_output = "Execution was forcefully terminated due to timeout."
                    
            except Exception as e:
                success = False
                status = "Failed"
                error_msg = f"Subprocess Error: {str(e)}"
                
        except Exception as e:
            success = False
            status = "Failed"
            error_msg = f"Execution engine error: {str(e)}"
            
        finally:
            try:
                if 'filepath' in locals() and os.path.exists(filepath):
                    os.remove(filepath)
                # Cleanup executables
                if sys.platform == "win32" and 'filepath' in locals():
                    exe_path = filepath.rsplit('.', 1)[0] + ".exe"
                    if os.path.exists(exe_path):
                        os.remove(exe_path)
                elif 'filepath' in locals():
                    exe_path = filepath.rsplit('.', 1)[0]
                    if os.path.exists(exe_path):
                        os.remove(exe_path)
                    class_path = filepath.replace('.java', '.class')
                    if os.path.exists(class_path):
                        os.remove(class_path)
            except Exception:
                pass
                
        # Final combined output for backward compatibility
        combined_output = ""
        if compilation_output:
            combined_output += f"--- Compilation Output ---\n{compilation_output.strip()}\n\n"
            
        if success and not runtime_output.strip():
            runtime_output = "Program executed successfully but produced no output."
            
        if runtime_output:
            combined_output += f"--- Runtime Output ---\n{runtime_output.strip()}"
            
        if error_msg and not success:
            combined_output += f"\n\n--- Error ---\n{error_msg}"
            
        return CodeExecutionResult(
            success=success,
            status=status,
            output=combined_output.strip() if combined_output else "No output",
            compilation_output=compilation_output.strip() if compilation_output else None,
            runtime_output=runtime_output.strip() if runtime_output else None,
            error=error_msg,
            execution_time=round(time.time() - start_time, 2)
        )

    def _get_file_extension(self, language: str) -> str:
        """Get file extension for language"""
        extensions = {
            "python": "py",
            "javascript": "js",
            "java": "java",
            "cpp": "cpp",
            "c": "c"
        }
        return extensions.get(language.lower(), "py")
    
    def test_code(self, code: str, test_code: str, language: str = "python") -> Dict[str, Any]:
        """Execute code with tests"""
        try:
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
                "error": str(e),
                "execution_time": 0
            }
