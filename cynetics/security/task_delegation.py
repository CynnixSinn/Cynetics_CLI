import subprocess
import tempfile
import os
import json
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

class ExecutionEnvironment(Enum):
    """Enumeration of execution environments."""
    LOCAL = "local"
    SANDBOX = "sandbox"
    CONTAINER = "container"

@dataclass
class Task:
    """A task to be executed."""
    id: str
    name: str
    description: str
    command: str
    environment: ExecutionEnvironment
    timeout: int = 30
    working_dir: Optional[str] = None
    allowed_paths: Optional[List[str]] = None
    created_at: float = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()

class SecureTaskDelegator:
    """A system for secure agentic task delegation."""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.task_results: Dict[str, Dict[str, Any]] = {}
        self.sandbox_dir = Path.home() / ".cynetics" / "sandboxes"
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)
    
    def create_task(self, name: str, description: str, command: str, 
                   environment: ExecutionEnvironment = ExecutionEnvironment.SANDBOX,
                   timeout: int = 30, working_dir: str = None, 
                   allowed_paths: List[str] = None) -> Task:
        """Create a new task.
        
        Args:
            name: Name of the task
            description: Description of the task
            command: Command to execute
            environment: Execution environment
            timeout: Timeout in seconds
            working_dir: Working directory
            allowed_paths: Allowed paths for file access
            
        Returns:
            Created task
        """
        import uuid
        task_id = str(uuid.uuid4())
        
        task = Task(
            id=task_id,
            name=name,
            description=description,
            command=command,
            environment=environment,
            timeout=timeout,
            working_dir=working_dir,
            allowed_paths=allowed_paths
        )
        
        self.tasks[task_id] = task
        return task
    
    def execute_task(self, task_id: str) -> Dict[str, Any]:
        """Execute a task securely.
        
        Args:
            task_id: ID of the task to execute
            
        Returns:
            Execution result
        """
        if task_id not in self.tasks:
            raise ValueError(f"Task with ID {task_id} not found")
        
        task = self.tasks[task_id]
        result = {
            "task_id": task_id,
            "task_name": task.name,
            "status": "pending",
            "start_time": time.time(),
            "end_time": None,
            "stdout": "",
            "stderr": "",
            "returncode": None,
            "error": None
        }
        
        try:
            if task.environment == ExecutionEnvironment.LOCAL:
                result.update(self._execute_local(task))
            elif task.environment == ExecutionEnvironment.SANDBOX:
                result.update(self._execute_sandbox(task))
            elif task.environment == ExecutionEnvironment.CONTAINER:
                result.update(self._execute_container(task))
            else:
                raise ValueError(f"Unsupported execution environment: {task.environment}")
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        finally:
            result["end_time"] = time.time()
            self.task_results[task_id] = result
        
        return result
    
    def _execute_local(self, task: Task) -> Dict[str, Any]:
        """Execute a task in the local environment."""
        result = {"status": "running"}
        
        try:
            # Change working directory if specified
            original_cwd = os.getcwd()
            if task.working_dir:
                os.chdir(task.working_dir)
            
            # Execute the command
            process = subprocess.Popen(
                task.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for completion with timeout
            stdout, stderr = process.communicate(timeout=task.timeout)
            
            result.update({
                "status": "completed",
                "stdout": stdout,
                "stderr": stderr,
                "returncode": process.returncode
            })
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            result.update({
                "status": "timeout",
                "stdout": stdout,
                "stderr": stderr,
                "returncode": process.returncode
            })
        except Exception as e:
            result.update({
                "status": "error",
                "error": str(e)
            })
        finally:
            # Restore original working directory
            if task.working_dir:
                os.chdir(original_cwd)
        
        return result
    
    def _execute_sandbox(self, task: Task) -> Dict[str, Any]:
        """Execute a task in a sandboxed environment."""
        result = {"status": "running"}
        
        try:
            # Create a temporary directory for the sandbox
            with tempfile.TemporaryDirectory(dir=self.sandbox_dir) as sandbox_dir:
                # Change to sandbox directory
                original_cwd = os.getcwd()
                os.chdir(sandbox_dir)
                
                # Create allowed paths if specified
                if task.allowed_paths:
                    for path in task.allowed_paths:
                        if os.path.exists(path):
                            # Create a symbolic link to the allowed path
                            link_name = os.path.basename(path)
                            os.symlink(path, link_name)
                
                # Execute the command
                process = subprocess.Popen(
                    task.command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Wait for completion with timeout
                stdout, stderr = process.communicate(timeout=task.timeout)
                
                result.update({
                    "status": "completed",
                    "stdout": stdout,
                    "stderr": stderr,
                    "returncode": process.returncode
                })
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            result.update({
                "status": "timeout",
                "stdout": stdout,
                "stderr": stderr,
                "returncode": process.returncode
            })
        except Exception as e:
            result.update({
                "status": "error",
                "error": str(e)
            })
        finally:
            # Restore original working directory
            if 'original_cwd' in locals():
                os.chdir(original_cwd)
        
        return result
    
    def _execute_container(self, task: Task) -> Dict[str, Any]:
        """Execute a task in a container environment."""
        result = {"status": "running"}
        
        # This is a simplified implementation
        # In a real system, you would use Docker or another container runtime
        try:
            # Check if Docker is available
            subprocess.run(["docker", "--version"], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL, 
                          check=True)
            
            # Create a temporary script file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
                f.write("#!/bin/bash\n")
                f.write(task.command)
                script_path = f.name
            
            # Make the script executable
            os.chmod(script_path, 0o755)
            
            # Run the script in a container
            container_cmd = [
                "docker", "run", "--rm",
                "-v", f"{script_path}:/script.sh",
                "alpine:latest",
                "/bin/bash", "/script.sh"
            ]
            
            process = subprocess.Popen(
                container_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for completion with timeout
            stdout, stderr = process.communicate(timeout=task.timeout)
            
            result.update({
                "status": "completed",
                "stdout": stdout,
                "stderr": stderr,
                "returncode": process.returncode
            })
            
            # Clean up the temporary script
            os.unlink(script_path)
        except subprocess.CalledProcessError:
            result.update({
                "status": "error",
                "error": "Docker not available or container execution failed"
            })
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            result.update({
                "status": "timeout",
                "stdout": stdout,
                "stderr": stderr,
                "returncode": process.returncode
            })
        except Exception as e:
            result.update({
                "status": "error",
                "error": str(e)
            })
        
        return result
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Task or None if not found
        """
        return self.tasks.get(task_id)
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all tasks.
        
        Returns:
            List of task information
        """
        return [
            {
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "environment": task.environment.value,
                "timeout": task.timeout,
                "created_at": task.created_at
            }
            for task in self.tasks.values()
        ]
    
    def get_task_result(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get the result of a task execution.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Task result or None if not found
        """
        return self.task_results.get(task_id)