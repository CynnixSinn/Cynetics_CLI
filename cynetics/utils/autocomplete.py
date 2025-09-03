from typing import List, Dict, Any, Tuple
import re

class IntelligentAutocomplete:
    """An intelligent autocomplete system that suggests entire workflows."""
    
    def __init__(self):
        self.workflows = self._load_workflows()
        self.commands = self._load_commands()
    
    def _load_workflows(self) -> Dict[str, Dict[str, Any]]:
        """Load built-in workflows."""
        return {
            "git_setup": {
                "name": "Git Repository Setup",
                "description": "Set up a new Git repository with initial commit",
                "commands": [
                    "git init",
                    "git add .",
                    "git commit -m \"Initial commit\""
                ],
                "tags": ["git", "version control", "setup"]
            },
            "python_project": {
                "name": "Python Project Setup",
                "description": "Set up a new Python project with virtual environment",
                "commands": [
                    "python -m venv venv",
                    "source venv/bin/activate",  # Linux/Mac
                    "venv\\Scripts\\activate",    # Windows
                    "pip install --upgrade pip"
                ],
                "tags": ["python", "setup", "development"]
            },
            "docker_build": {
                "name": "Docker Build and Run",
                "description": "Build and run a Docker container",
                "commands": [
                    "docker build -t myapp .",
                    "docker run -p 8080:8080 myapp"
                ],
                "tags": ["docker", "container", "deployment"]
            },
            "web_scraping": {
                "name": "Web Scraping Workflow",
                "description": "Set up and run a web scraping project",
                "commands": [
                    "pip install requests beautifulsoup4 pandas",
                    "python scrape.py"
                ],
                "tags": ["web", "scraping", "data"]
            },
            "data_analysis": {
                "name": "Data Analysis Setup",
                "description": "Set up environment for data analysis",
                "commands": [
                    "pip install pandas numpy matplotlib seaborn jupyter",
                    "jupyter notebook"
                ],
                "tags": ["data", "analysis", "jupyter"]
            }
        }
    
    def _load_commands(self) -> Dict[str, Dict[str, Any]]:
        """Load command information."""
        return {
            "git": {
                "description": "Distributed version control system",
                "common_flags": ["init", "clone", "add", "commit", "push", "pull", "status", "log"],
                "workflows": ["git_setup"]
            },
            "python": {
                "description": "Python programming language interpreter",
                "common_flags": ["-m", "--version", "-c", "-V"],
                "workflows": ["python_project"]
            },
            "docker": {
                "description": "Container platform",
                "common_flags": ["build", "run", "ps", "images", "pull", "push"],
                "workflows": ["docker_build"]
            },
            "pip": {
                "description": "Python package installer",
                "common_flags": ["install", "list", "show", "uninstall", "freeze"],
                "workflows": ["web_scraping", "data_analysis"]
            },
            "ls": {
                "description": "List directory contents",
                "common_flags": ["-l", "-a", "-la", "-lh"],
                "workflows": []
            },
            "cd": {
                "description": "Change directory",
                "common_flags": [],
                "workflows": []
            },
            "mkdir": {
                "description": "Make directories",
                "common_flags": ["-p"],
                "workflows": []
            }
        }
    
    def suggest_workflows(self, partial_input: str) -> List[Dict[str, Any]]:
        """Suggest workflows based on partial input.
        
        Args:
            partial_input: Partial command input
            
        Returns:
            List of suggested workflows
        """
        suggestions = []
        
        # Check if the partial input matches any workflow tags
        for workflow_id, workflow in self.workflows.items():
            # Match by tag
            for tag in workflow["tags"]:
                if tag.startswith(partial_input.lower()):
                    suggestions.append({
                        "type": "workflow",
                        "id": workflow_id,
                        "name": workflow["name"],
                        "description": workflow["description"],
                        "commands": workflow["commands"],
                        "match_type": "tag"
                    })
                    break
            
            # Match by name
            if workflow["name"].lower().startswith(partial_input.lower()):
                # Check if we already added this workflow
                if not any(s["id"] == workflow_id for s in suggestions):
                    suggestions.append({
                        "type": "workflow",
                        "id": workflow_id,
                        "name": workflow["name"],
                        "description": workflow["description"],
                        "commands": workflow["commands"],
                        "match_type": "name"
                    })
        
        return suggestions
    
    def suggest_commands(self, partial_input: str) -> List[Dict[str, Any]]:
        """Suggest commands based on partial input.
        
        Args:
            partial_input: Partial command input
            
        Returns:
            List of suggested commands
        """
        suggestions = []
        
        # Check if the partial input matches any command names
        for cmd, info in self.commands.items():
            if cmd.startswith(partial_input.lower()):
                suggestions.append({
                    "type": "command",
                    "name": cmd,
                    "description": info["description"],
                    "common_flags": info["common_flags"],
                    "workflows": info["workflows"]
                })
        
        return suggestions
    
    def suggest_flags(self, command: str, partial_flag: str) -> List[str]:
        """Suggest flags for a command.
        
        Args:
            command: Command name
            partial_flag: Partial flag input
            
        Returns:
            List of suggested flags
        """
        if command in self.commands:
            flags = self.commands[command]["common_flags"]
            return [flag for flag in flags if flag.startswith(partial_flag)]
        return []
    
    def suggest_combined(self, partial_input: str) -> List[Dict[str, Any]]:
        """Provide combined suggestions including commands, flags, and workflows.
        
        Args:
            partial_input: Partial command input
            
        Returns:
            List of all relevant suggestions
        """
        suggestions = []
        
        # Parse the partial input
        parts = partial_input.strip().split()
        if not parts:
            return suggestions
        
        # If we have a command and are typing flags
        if len(parts) >= 2 and parts[0] in self.commands:
            command = parts[0]
            partial_flag = parts[-1] if parts[-1].startswith("-") else ""
            if partial_flag:
                flag_suggestions = self.suggest_flags(command, partial_flag)
                for flag in flag_suggestions:
                    suggestions.append({
                        "type": "flag",
                        "command": command,
                        "flag": flag,
                        "full_suggestion": f"{' '.join(parts[:-1])} {flag}"
                    })
        
        # Suggest commands
        command_suggestions = self.suggest_commands(parts[0])
        suggestions.extend(command_suggestions)
        
        # Suggest workflows
        workflow_suggestions = self.suggest_workflows(partial_input)
        suggestions.extend(workflow_suggestions)
        
        return suggestions
    
    def get_workflow_details(self, workflow_id: str) -> Dict[str, Any]:
        """Get detailed information about a workflow.
        
        Args:
            workflow_id: ID of the workflow
            
        Returns:
            Workflow details
        """
        return self.workflows.get(workflow_id, {})
    
    def get_command_details(self, command: str) -> Dict[str, Any]:
        """Get detailed information about a command.
        
        Args:
            command: Command name
            
        Returns:
            Command details
        """
        return self.commands.get(command, {})
    
    def search_workflows(self, query: str) -> List[Dict[str, Any]]:
        """Search workflows by query.
        
        Args:
            query: Search query
            
        Returns:
            List of matching workflows
        """
        results = []
        query_lower = query.lower()
        
        for workflow_id, workflow in self.workflows.items():
            # Match by name, description, or tags
            if (query_lower in workflow["name"].lower() or 
                query_lower in workflow["description"].lower() or
                any(query_lower in tag for tag in workflow["tags"])):
                results.append({
                    "id": workflow_id,
                    "name": workflow["name"],
                    "description": workflow["description"],
                    "tags": workflow["tags"]
                })
        
        return results