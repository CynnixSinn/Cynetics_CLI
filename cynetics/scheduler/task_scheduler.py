import time
import threading
from typing import Callable, Dict, Any
from datetime import datetime, timedelta
from queue import Queue, Empty

class TaskScheduler:
    """A simple task scheduler for running tasks at specific times or intervals."""
    
    def __init__(self):
        self.tasks = {}
        self.task_queue = Queue()
        self.running = False
        self.scheduler_thread = None
        self.task_counter = 0
    
    def start(self):
        """Start the scheduler."""
        if not self.running:
            self.running = True
            self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
            self.scheduler_thread.start()
    
    def stop(self):
        """Stop the scheduler."""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
    
    def _scheduler_loop(self):
        """Main scheduler loop."""
        while self.running:
            try:
                # Check for scheduled tasks
                current_time = datetime.now()
                tasks_to_execute = []
                
                for task_id, task_info in list(self.tasks.items()):
                    if task_info["next_run"] <= current_time:
                        tasks_to_execute.append(task_id)
                        
                        # Reschedule repeating tasks
                        if task_info["repeat"]:
                            task_info["next_run"] = current_time + task_info["interval"]
                        else:
                            # Remove one-time tasks after execution
                            del self.tasks[task_id]
                
                # Execute tasks
                for task_id in tasks_to_execute:
                    task_info = self.tasks.get(task_id)
                    if task_info:
                        try:
                            result = task_info["function"](*task_info["args"], **task_info["kwargs"])
                            task_info["last_result"] = result
                            task_info["last_run"] = current_time
                        except Exception as e:
                            task_info["last_error"] = str(e)
                
                # Sleep briefly to avoid busy waiting
                time.sleep(0.01)  # Reduced sleep time
                
            except Exception as e:
                print(f"Scheduler error: {e}")
                # Continue running even if there's an error
    
    def schedule_task(self, function: Callable, run_at: datetime = None, 
                     interval: timedelta = None, repeat: bool = False,
                     args: tuple = (), kwargs: dict = None) -> int:
        """Schedule a task to run at a specific time or interval.
        
        Args:
            function: The function to execute
            run_at: When to run the task (default: now)
            interval: How often to repeat the task
            repeat: Whether to repeat the task
            args: Arguments to pass to the function
            kwargs: Keyword arguments to pass to the function
            
        Returns:
            Task ID
        """
        if kwargs is None:
            kwargs = {}
            
        self.task_counter += 1
        task_id = self.task_counter
        
        if run_at is None:
            run_at = datetime.now()
            
        if interval is None and repeat:
            interval = timedelta(seconds=1)  # Shorter default interval
            
        self.tasks[task_id] = {
            "function": function,
            "args": args,
            "kwargs": kwargs,
            "next_run": run_at,
            "interval": interval,
            "repeat": repeat,
            "created_at": datetime.now(),
            "last_run": None,
            "last_result": None,
            "last_error": None
        }
        
        return task_id
    
    def cancel_task(self, task_id: int) -> bool:
        """Cancel a scheduled task."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False
    
    def list_tasks(self) -> Dict[int, Dict[str, Any]]:
        """List all scheduled tasks."""
        return self.tasks.copy()
    
    def get_task_info(self, task_id: int) -> Dict[str, Any]:
        """Get information about a specific task."""
        return self.tasks.get(task_id, None)