import click
import json
import os
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
from uuid import uuid4

class PlaybookManager:
    """Contextual playbooks system."""
    
    def __init__(self, storage_dir: str = "playbooks"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.playbooks_file = self.storage_dir / "playbooks.json"
        self._load_playbooks()
    
    def _load_playbooks(self):
        """Load playbooks from file."""
        if self.playbooks_file.exists():
            with open(self.playbooks_file, 'r') as f:
                self.playbooks = json.load(f)
        else:
            self.playbooks = {}
            self._save_playbooks()
    
    def _save_playbooks(self):
        """Save playbooks to file."""
        with open(self.playbooks_file, 'w') as f:
            json.dump(self.playbooks, f, indent=2)
    
    def create_playbook(self, name: str, description: str, steps_file: str, tags: List[str] = None) -> str:
        """Create a new playbook."""
        # Read steps from YAML file
        if not os.path.exists(steps_file):
            raise FileNotFoundError(f"Steps file '{steps_file}' not found")
        
        with open(steps_file, 'r') as f:
            steps_data = yaml.safe_load(f)
        
        playbook_id = str(uuid4())
        
        playbook = {
            "id": playbook_id,
            "name": name,
            "description": description,
            "steps": steps_data.get("steps", []),
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
            "execution_count": 0,
            "last_executed": None
        }
        
        self.playbooks[playbook_id] = playbook
        self._save_playbooks()
        
        return playbook_id
    
    def list_playbooks(self) -> Dict[str, Dict[str, Any]]:
        """List all playbooks."""
        return self.playbooks
    
    def get_playbook(self, playbook_id: str) -> Dict[str, Any]:
        """Get a playbook by ID."""
        return self.playbooks.get(playbook_id, None)
    
    def show_playbook(self, playbook_id: str) -> Dict[str, Any]:
        """Show detailed information about a playbook."""
        return self.get_playbook(playbook_id)
    
    def execute_playbook(self, playbook_id: str, dry_run: bool = False) -> Dict[str, Any]:
        """Execute a playbook."""
        if playbook_id not in self.playbooks:
            raise ValueError(f"Playbook '{playbook_id}' not found")
        
        playbook = self.playbooks[playbook_id]
        
        results = {
            "playbook_id": playbook_id,
            "playbook_name": playbook["name"],
            "dry_run": dry_run,
            "steps": []
        }
        
        # Update execution count and last executed time
        playbook["execution_count"] += 1
        playbook["last_executed"] = datetime.now().isoformat()
        self._save_playbooks()
        
        # Execute each step
        for i, step in enumerate(playbook["steps"]):
            step_result = {
                "step_number": i + 1,
                "name": step.get("name", f"Step {i + 1}"),
                "command": step.get("command"),
                "description": step.get("description")
            }
            
            if dry_run:
                step_result["status"] = "dry_run"
                step_result["message"] = "Would execute command"
            else:
                # In a real implementation, you would execute the command here
                step_result["status"] = "simulated"
                step_result["message"] = "Command execution simulated (not implemented in this demo)"
            
            results["steps"].append(step_result)
        
        return results

@click.command()
@click.option('--list', 'list_playbooks', is_flag=True, help='List all playbooks')
@click.option('--create', is_flag=True, help='Create a new playbook')
@click.option('--execute', help='Execute a playbook by ID')
@click.option('--show', help='Show detailed information about a playbook')
@click.option('--name', help='Name of the playbook')
@click.option('--description', help='Description of the playbook')
@click.option('--steps-file', help='YAML file containing playbook steps')
@click.option('--tags', multiple=True, help='Tags for the playbook')
@click.option('--dry-run', is_flag=True, help='Preview execution without running commands')
def playbooks(list_playbooks, create, execute, show, name, description, steps_file, tags, dry_run):
    """Execute recurring multi-step tasks."""
    manager = PlaybookManager()
    
    if list_playbooks:
        playbooks_data = manager.list_playbooks()
        if not playbooks_data:
            click.echo("No playbooks available.")
            return
        
        click.echo("Available playbooks:")
        for playbook_id, playbook in playbooks_data.items():
            click.echo(f"  {playbook['name']} ({playbook_id})")
            click.echo(f"    Description: {playbook['description']}")
            if playbook.get('tags'):
                click.echo(f"    Tags: {', '.join(playbook['tags'])}")
            click.echo(f"    Steps: {len(playbook['steps'])}")
            click.echo(f"    Executed: {playbook['execution_count']} times")
            if playbook['last_executed']:
                click.echo(f"    Last executed: {playbook['last_executed']}")
            click.echo()
    
    elif create:
        if not name or not description or not steps_file:
            click.echo("Error: --name, --description, and --steps-file are required to create a playbook")
            return
        
        try:
            playbook_id = manager.create_playbook(name, description, steps_file, list(tags))
            click.echo(f"Created playbook: {playbook_id}")
            click.echo(f"  Name: {name}")
            click.echo(f"  Description: {description}")
        except Exception as e:
            click.echo(f"Error creating playbook: {e}")
    
    elif execute:
        try:
            results = manager.execute_playbook(execute, dry_run)
            click.echo(f"Playbook execution {'(dry run)' if dry_run else ''}: {results['playbook_name']}")
            
            for step in results["steps"]:
                status_icon = {
                    "dry_run": "○",
                    "simulated": "◐",
                    "success": "●",
                    "failed": "✗"
                }.get(step["status"], "?")
                
                click.echo(f"  {status_icon} Step {step['step_number']}: {step['name']}")
                if step.get('command'):
                    click.echo(f"    Command: {step['command']}")
                if step.get('description'):
                    click.echo(f"    Description: {step['description']}")
                click.echo(f"    Status: {step['status']}")
                if step.get('message'):
                    click.echo(f"    Message: {step['message']}")
                click.echo()
        except Exception as e:
            click.echo(f"Error executing playbook: {e}")
    
    elif show:
        try:
            playbook = manager.show_playbook(show)
            if not playbook:
                click.echo(f"Playbook '{show}' not found.")
                return
            
            click.echo(f"Playbook: {playbook['name']}")
            click.echo(f"  ID: {playbook['id']}")
            click.echo(f"  Description: {playbook['description']}")
            if playbook.get('tags'):
                click.echo(f"  Tags: {', '.join(playbook['tags'])}")
            click.echo(f"  Created: {playbook['created_at']}")
            click.echo(f"  Executed: {playbook['execution_count']} times")
            if playbook['last_executed']:
                click.echo(f"  Last executed: {playbook['last_executed']}")
            click.echo()
            click.echo("Steps:")
            for i, step in enumerate(playbook['steps']):
                click.echo(f"  {i + 1}. {step.get('name', f'Step {i + 1}')}")
                if step.get('description'):
                    click.echo(f"     Description: {step['description']}")
                if step.get('command'):
                    click.echo(f"     Command: {step['command']}")
                click.echo()
        except Exception as e:
            click.echo(f"Error showing playbook: {e}")
    
    else:
        click.echo("Contextual Playbooks System")
        click.echo("Use --list to see available playbooks, --create to create a new playbook, or --execute to run a playbook.")

if __name__ == "__main__":
    playbooks()