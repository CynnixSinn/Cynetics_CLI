import click
import json
import os
from pathlib import Path
from typing import Dict, Any

class TutorialManager:
    """AI-driven CLI tutorial system."""
    
    def __init__(self, storage_dir: str = "tutorials"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.progress_file = self.storage_dir / "progress.json"
        self._load_progress()
        
        # Built-in tutorials
        self.tutorials = {
            "basic_navigation": {
                "title": "Basic Navigation",
                "description": "Learn basic file navigation commands",
                "difficulty": "beginner",
                "commands": ["ls", "cd", "pwd"],
                "content": """
In this tutorial, you'll learn basic navigation commands:
1. 'ls' - List directory contents
2. 'cd' - Change directory
3. 'pwd' - Print working directory

Practice these commands in your terminal.
                """.strip()
            },
            "file_operations": {
                "title": "File Operations",
                "description": "Learn basic file operations",
                "difficulty": "beginner",
                "commands": ["touch", "cp", "mv", "rm"],
                "content": """
In this tutorial, you'll learn basic file operations:
1. 'touch' - Create empty files
2. 'cp' - Copy files
3. 'mv' - Move/rename files
4. 'rm' - Remove files

Practice these commands in your terminal.
                """.strip()
            },
            "process_management": {
                "title": "Process Management",
                "description": "Learn process management commands",
                "difficulty": "intermediate",
                "commands": ["ps", "kill", "top", "htop"],
                "content": """
In this tutorial, you'll learn process management commands:
1. 'ps' - List running processes
2. 'kill' - Terminate processes
3. 'top' - Display system processes
4. 'htop' - Interactive process viewer

Practice these commands in your terminal.
                """.strip()
            }
        }
    
    def _load_progress(self):
        """Load tutorial progress from file."""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                self.progress = json.load(f)
        else:
            self.progress = {}
            self._save_progress()
    
    def _save_progress(self):
        """Save tutorial progress to file."""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def list_tutorials(self) -> Dict[str, Dict[str, Any]]:
        """List all available tutorials."""
        return self.tutorials
    
    def get_tutorial(self, name: str) -> Dict[str, Any]:
        """Get a tutorial by name."""
        return self.tutorials.get(name, None)
    
    def start_tutorial(self, name: str) -> Dict[str, Any]:
        """Start a tutorial."""
        if name not in self.tutorials:
            raise ValueError(f"Tutorial '{name}' not found")
        
        tutorial = self.tutorials[name]
        
        # Mark as in progress
        from datetime import datetime
        self.progress[name] = {
            "status": "in_progress",
            "started_at": datetime.now().isoformat()
        }
        self._save_progress()
        
        return tutorial
    
    def complete_tutorial(self, name: str):
        """Mark a tutorial as completed."""
        if name not in self.tutorials:
            raise ValueError(f"Tutorial '{name}' not found")
        
        from datetime import datetime
        self.progress[name] = {
            "status": "completed",
            "completed_at": datetime.now().isoformat(),
            "started_at": self.progress.get(name, {}).get("started_at", datetime.now().isoformat())
        }
        self._save_progress()
    
    def get_progress(self) -> Dict[str, Any]:
        """Get tutorial progress."""
        return self.progress
    
    def recommend_tutorial(self) -> str:
        """Recommend a tutorial based on progress."""
        # Find tutorials that haven't been started
        not_started = [name for name in self.tutorials if name not in self.progress]
        if not_started:
            return not_started[0]
        
        # Find tutorials that are in progress
        in_progress = [name for name, progress in self.progress.items() 
                      if progress.get("status") == "in_progress"]
        if in_progress:
            return in_progress[0]
        
        # If all tutorials are completed, recommend the first one
        return list(self.tutorials.keys())[0] if self.tutorials else None

@click.command()
@click.option('--list', 'list_tutorials', is_flag=True, help='List available tutorials')
@click.option('--start', help='Start an interactive tutorial')
@click.option('--complete', help='Mark a tutorial as completed')
@click.option('--progress', is_flag=True, help='Show tutorial progress')
@click.option('--recommend', is_flag=True, help='Get a recommended tutorial')
def cli_tutorial(list_tutorials, start, complete, progress, recommend):
    """Learn new shell commands interactively."""
    manager = TutorialManager()
    
    if list_tutorials:
        tutorials = manager.list_tutorials()
        if not tutorials:
            click.echo("No tutorials available.")
            return
        
        click.echo("Available tutorials:")
        for name, tutorial in tutorials.items():
            status = manager.progress.get(name, {}).get("status", "not_started")
            status_icon = {
                "not_started": "○",
                "in_progress": "◐",
                "completed": "●"
            }.get(status, "○")
            
            click.echo(f"  {status_icon} {tutorial['title']} ({name})")
            click.echo(f"    Difficulty: {tutorial['difficulty']}")
            click.echo(f"    Description: {tutorial['description']}")
            click.echo(f"    Commands: {', '.join(tutorial['commands'])}")
            click.echo()
    
    elif start:
        try:
            tutorial = manager.start_tutorial(start)
            click.echo(f"Starting tutorial: {tutorial['title']}")
            click.echo(f"Difficulty: {tutorial['difficulty']}")
            click.echo()
            click.echo(tutorial['content'])
            click.echo()
            click.echo("Practice the commands mentioned above.")
            click.echo("When you're done, use --complete to mark this tutorial as completed.")
        except Exception as e:
            click.echo(f"Error starting tutorial: {e}")
    
    elif complete:
        try:
            manager.complete_tutorial(complete)
            click.echo(f"Tutorial '{complete}' marked as completed!")
        except Exception as e:
            click.echo(f"Error completing tutorial: {e}")
    
    elif progress:
        progress_data = manager.get_progress()
        if not progress_data:
            click.echo("No tutorial progress found.")
            return
        
        click.echo("Tutorial Progress:")
        for name, data in progress_data.items():
            tutorial = manager.get_tutorial(name)
            if tutorial:
                title = tutorial.get('title', name)
                status = data.get('status', 'unknown')
                click.echo(f"  {title}: {status}")
    
    elif recommend:
        recommendation = manager.recommend_tutorial()
        if recommendation:
            tutorial = manager.get_tutorial(recommendation)
            click.echo(f"Recommended tutorial: {tutorial['title']} ({recommendation})")
            click.echo(f"Description: {tutorial['description']}")
            click.echo(f"Difficulty: {tutorial['difficulty']}")
        else:
            click.echo("No tutorials available for recommendation.")
    
    else:
        click.echo("AI-Driven CLI Tutorial System")
        click.echo("Use --list to see available tutorials, --start to begin a tutorial, or --recommend to get a recommendation.")

if __name__ == "__main__":
    cli_tutorial()