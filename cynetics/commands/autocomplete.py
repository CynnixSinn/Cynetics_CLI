import click
import json
import os
from pathlib import Path
from typing import Dict, Any, List

class WorkflowManager:
    """Intelligent autocomplete and workflow system."""
    
    def __init__(self, storage_dir: str = "workflows"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.workflows_file = self.storage_dir / "workflows.json"
        self._load_workflows()
        
        # Built-in workflows
        if not self.workflows:
            self.workflows = {
                "git_setup": {
                    "name": "Git Setup",
                    "description": "Set up a new Git repository",
                    "tags": ["git", "version_control"],
                    "steps": [
                        "mkdir project_name",
                        "cd project_name",
                        "git init",
                        "echo '# Project Name' > README.md",
                        "git add README.md",
                        "git commit -m 'Initial commit'"
                    ]
                },
                "docker_build": {
                    "name": "Docker Build",
                    "description": "Build and run a Docker container",
                    "tags": ["docker", "containerization"],
                    "steps": [
                        "docker build -t app_name .",
                        "docker run -p 8080:8080 app_name"
                    ]
                },
                "python_env": {
                    "name": "Python Environment",
                    "description": "Set up a Python virtual environment",
                    "tags": ["python", "development"],
                    "steps": [
                        "python -m venv venv",
                        "source venv/bin/activate",
                        "pip install -r requirements.txt"
                    ]
                }
            }
            self._save_workflows()
    
    def _load_workflows(self):
        """Load workflows from file."""
        if self.workflows_file.exists():
            with open(self.workflows_file, 'r') as f:
                self.workflows = json.load(f)
        else:
            self.workflows = {}
    
    def _save_workflows(self):
        """Save workflows to file."""
        with open(self.workflows_file, 'w') as f:
            json.dump(self.workflows, f, indent=2)
    
    def create_workflow(self, name: str, description: str, steps: List[str], tags: List[str] = None) -> Dict[str, Any]:
        """Create a new workflow."""
        workflow = {
            "name": name,
            "description": description,
            "steps": steps,
            "tags": tags or []
        }
        
        self.workflows[name] = workflow
        self._save_workflows()
        
        return workflow
    
    def list_workflows(self) -> Dict[str, Dict[str, Any]]:
        """List all workflows."""
        return self.workflows
    
    def get_workflow(self, name: str) -> Dict[str, Any]:
        """Get a workflow by name."""
        return self.workflows.get(name, None)
    
    def search_workflows(self, query: str) -> Dict[str, Dict[str, Any]]:
        """Search workflows by name, description, or tags."""
        results = {}
        query = query.lower()
        
        for name, workflow in self.workflows.items():
            # Check name, description, and tags
            if (query in name.lower() or 
                query in workflow.get("description", "").lower() or
                any(query in tag.lower() for tag in workflow.get("tags", []))):
                results[name] = workflow
        
        return results
    
    def suggest_commands(self, partial_command: str) -> List[str]:
        """Suggest commands based on partial input."""
        suggestions = []
        partial_lower = partial_command.lower()
        
        # Check built-in commands
        built_in_commands = ["ls", "cd", "pwd", "git", "docker", "python", "pip", "npm", "curl", "wget"]
        suggestions.extend([cmd for cmd in built_in_commands if cmd.startswith(partial_lower)])
        
        # Check workflow names
        suggestions.extend([name for name in self.workflows if name.startswith(partial_lower)])
        
        return suggestions[:10]  # Limit to 10 suggestions

@click.command()
@click.option('--suggest', help='Get suggestions for a partial command')
@click.option('--workflows', is_flag=True, help='List all workflows')
@click.option('--search-workflows', help='Search workflows by keyword')
@click.option('--create-workflow', is_flag=True, help='Create a new workflow')
@click.option('--name', help='Name of the workflow')
@click.option('--description', help='Description of the workflow')
@click.option('--steps-file', help='File containing workflow steps (one per line)')
@click.option('--tags', multiple=True, help='Tags for the workflow')
def autocomplete(suggest, workflows, search_workflows, create_workflow, name, description, steps_file, tags):
    """Get suggestions for entire workflows."""
    manager = WorkflowManager()
    
    if suggest:
        suggestions = manager.suggest_commands(suggest)
        if suggestions:
            click.echo("Command suggestions:")
            for suggestion in suggestions:
                click.echo(f"  {suggestion}")
        else:
            click.echo("No suggestions found.")
    
    elif workflows:
        workflows_data = manager.list_workflows()
        if not workflows_data:
            click.echo("No workflows available.")
            return
        
        click.echo("Available workflows:")
        for name, workflow in workflows_data.items():
            click.echo(f"  {workflow['name']} ({name})")
            click.echo(f"    Description: {workflow['description']}")
            if workflow.get('tags'):
                click.echo(f"    Tags: {', '.join(workflow['tags'])}")
            click.echo(f"    Steps: {len(workflow['steps'])}")
            click.echo()
    
    elif search_workflows:
        results = manager.search_workflows(search_workflows)
        if not results:
            click.echo(f"No workflows found matching '{search_workflows}'.")
            return
        
        click.echo(f"Workflows matching '{search_workflows}':")
        for name, workflow in results.items():
            click.echo(f"  {workflow['name']} ({name})")
            click.echo(f"    Description: {workflow['description']}")
            if workflow.get('tags'):
                click.echo(f"    Tags: {', '.join(workflow['tags'])}")
            click.echo()
    
    elif create_workflow:
        if not name or not description or not steps_file:
            click.echo("Error: --name, --description, and --steps-file are required to create a workflow")
            return
        
        if not os.path.exists(steps_file):
            click.echo(f"Error: Steps file '{steps_file}' not found")
            return
        
        # Read steps from file
        with open(steps_file, 'r') as f:
            steps = [line.strip() for line in f.readlines() if line.strip()]
        
        try:
            workflow = manager.create_workflow(name, description, steps, list(tags))
            click.echo(f"Created workflow: {workflow['name']}")
            click.echo(f"  Description: {workflow['description']}")
            click.echo(f"  Steps: {len(workflow['steps'])}")
            if workflow.get('tags'):
                click.echo(f"  Tags: {', '.join(workflow['tags'])}")
        except Exception as e:
            click.echo(f"Error creating workflow: {e}")
    
    else:
        click.echo("Intelligent Autocomplete System")
        click.echo("Use --suggest to get command suggestions, --workflows to list workflows, or --search-workflows to search.")

if __name__ == "__main__":
    autocomplete()