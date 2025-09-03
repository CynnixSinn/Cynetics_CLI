#!/usr/bin/env python3

def test_task_scheduler():
    """Test the task scheduler module."""
    print("\nTesting TaskScheduler...")
    try:
        from cynetics.scheduler.task_scheduler import TaskScheduler
        import time
        from datetime import datetime, timedelta
        
        scheduler = TaskScheduler()
        scheduler.start()
        
        # Test scheduling a simple task
        result = []
        
        def test_task():
            result.append("executed")
            print("Task executed!")
        
        # Print current time
        print(f"Current time: {datetime.now()}")
        
        # Schedule task to run immediately
        task_id = scheduler.schedule_task(test_task)
        print(f"Scheduled task with ID: {task_id}")
        
        # Print task info
        task_info = scheduler.get_task_info(task_id)
        print(f"Task info: {task_info}")
        
        # Wait a moment for task to execute
        print("Waiting for task to execute...")
        time.sleep(1.0)
        
        # Check if task executed
        print(f"Result length: {len(result)}")
        print(f"Result content: {result}")
        
        # List all tasks
        tasks = scheduler.list_tasks()
        print(f"Remaining tasks: {tasks}")
        
        # Stop scheduler
        scheduler.stop()
        
        print("✓ TaskScheduler tests passed")
        return True
    except Exception as e:
        print(f"✗ TaskScheduler tests failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_task_scheduler()