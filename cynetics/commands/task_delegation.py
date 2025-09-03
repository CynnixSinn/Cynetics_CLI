import click
import json
import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class SecureTaskDelegation:
    """Secure task delegation system."""
    
    def __init__(self, storage_dir: str = "tasks"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.tasks_file = self.storage_dir / "tasks.json"
        self._load_tasks()
    
    def _load_tasks(self):
        """Load tasks from file."""
        if self.tasks_file.exists():
            with open(self.tasks_file, 'r') as f:
                self.tasks = json.load(f)
        else:
            self.tasks = {}
            self._save_tasks()
    
    def _save_tasks(self):
        """Save tasks to file."""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def create_task(self, name: str, description: str, command: str, environment: str = "local") -> str:
        """Create a new task."""
        from uuid import uuid4
        
        task_id = str(uuid4())
        
        task = {
            "id": task_id,
            "name": name,
            "description": description,
            "command": command,
            "environment": environment,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "executed_at": None,
            "result": None
        }
        
        self.tasks[task_id] = task
        self._save_tasks()
        
        return task_id
    
    def list_tasks(self) -> Dict[str, Dict[str, Any]]:
        """List all tasks."""
        return self.tasks
    
    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get a task by ID."""
        return self.tasks.get(task_id, None)
    
    def execute_task(self, task_id: str) -> Dict[str, Any]:
        """Execute a task securely."""
        if task_id not in self.tasks:
            raise ValueError(f"Task '{task_id}' not found")
        
        task = self.tasks[task_id]
        
        try:
            # Update task status
            task["status"] = "running"
            task["executed_at"] = datetime.now().isoformat()
            self._save_tasks()
            
            # Execute based on environment
            if task["environment"] == "local":
                result = self._execute_local(task["command"])
            elif task["environment"] == "sandbox":
                result = self._execute_sandboxed(task["command"])
            elif task["environment"] == "container":
                result = self._execute_containerized(task["command"])
            else:
                raise ValueError(f"Unsupported environment: {task['environment']}")
            
            # Update task with result
            task["status"] = "completed"
            task["result"] = result
            self._save_tasks()
            
            return result
            
        except Exception as e:
            task["status"] = "failed"
            task["result"] = {"error": str(e)}
            self._save_tasks()
            raise
    
    def _execute_local(self, command: str) -> Dict[str, Any]:
        """Execute command in local environment."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {"error": "Command timed out"}
        except Exception as e:
            return {"error": str(e)}
    
    def _execute_sandboxed(self, command: str) -> Dict[str, Any]:
        """Execute command in a sandboxed environment."""
        # Create a temporary directory for sandboxing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Change to temp directory
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Execute command with restricted permissions
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                return {
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "success": result.returncode == 0,
                    "sandbox_path": temp_dir
                }
            except subprocess.TimeoutExpired:
                return {"error": "Command timed out"}
            except Exception as e:
                return {"error": str(e)}
            finally:
                os.chdir(original_cwd)
    
    def _execute_containerized(self, command: str) -> Dict[str, Any]:
        """Execute command in a containerized environment."""
        # This is a simplified version - in a real implementation,
        # you would use Docker or another containerization technology
        return {
            "message": "Containerized execution not yet implemented",
            "command": command,
            "environment": "container"
        }

@click.command()
@click.option('--create', is_flag=True, help='Create a new task')
@click.option('--execute', help='Execute a task by ID')
@click.option('--list-tasks', is_flag=True, help='List all tasks')
@click.option('--name', help='Name of the task')
@click.option('--description', help='Description of the task')
@click.option('--command', help='Command to execute')
@click.option('--environment', default='local', type=click.Choice(['local', 'sandbox', 'container']), help='Execution environment')
def task_delegation(create, execute, list_tasks, name, description, command, environment):
    """Execute tasks in secure environments."""
    manager = SecureTaskDelegation()
    
    if create:
        if not name or not description or not command:
            click.echo("Error: --name, --description, and --command are required to create a task")
            return
        
        task_id = manager.create_task(name, description, command, environment)
        click.echo(f"Created task: {task_id}")
        click.echo(f"  Name: {name}")
        click.echo(f"  Environment: {environment}")
        click.echo(f"  Status: pending")
    
    elif execute:
        try:
            click.echo(f"Executing task '{execute}'...")
            result = manager.execute_task(execute)
            
            task = manager.get_task(execute)
            click.echo(f"Task execution completed")
            click.echo(f"  Status: {task['status']}")
            
            if "error" in result:
                click.echo(f"  Error: {result['error']}")
            else:
                click.echo(f"  Success: {result.get('success', 'N/A')}")
                click.echo(f"  Return code: {result.get('returncode', 'N/A')}")
                if result.get('stdout'):
                    click.echo(f"  Output: {result['stdout']}")
                if result.get('stderr'):
                    click.echo(f"  Errors: {result['stderr']}")
        except Exception as e:
            click.echo(f"Error executing task: {e}")
    
    elif list_tasks:
        tasks = manager.list_tasks()
        if not tasks:
            click.echo("No tasks found.")
            return
        
        click.echo("Available tasks:")
        for task_id, task_data in tasks.items():
            status_icon = {
                "pending": "○",
                "running": "◐",
                "completed": "●",
                "failed": "✗"
            }.get(task_data["status"], "?")
            
            click.echo(f"  {status_icon} {task_data['name']} ({task_id})")
            click.echo(f"    Description: {task_data['description']}")
            click.echo(f"    Environment: {task_data['environment']}")
            click.echo(f"    Status: {task_data['status']}")
            click.echo(f"    Created: {task_data['created_at']}")
            if task_data['executed_at']:
                click.echo(f"    Executed: {task_data['executed_at']}")
            click.echo()
    
    else:
        click.echo("Secure Task Delegation System")
        click.echo("Use --create to create a new task, --execute to run a task, or --list-tasks to see all tasks.")

if __name__ == "__main__":
    task_delegation()