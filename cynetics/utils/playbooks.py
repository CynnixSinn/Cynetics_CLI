import yaml
import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PlaybookStep:
    """A step in a playbook."""
    name: str
    description: str
    command: str
    expected_output: Optional[str] = None
    timeout: int = 30
    continue_on_error: bool = False

@dataclass
class Playbook:
    """A playbook for recurring multi-step tasks."""
    id: str
    name: str
    description: str
    steps: List[PlaybookStep]
    tags: List[str]
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

class PlaybookManager:
    """Manager for contextual playbooks."""
    
    def __init__(self, playbooks_dir: str = "playbooks"):
        self.playbooks_dir = Path(playbooks_dir)
        self.playbooks_dir.mkdir(exist_ok=True)
        self.playbooks: Dict[str, Playbook] = {}
        self._load_playbooks()
    
    def _load_playbooks(self):
        """Load playbooks from the playbooks directory."""
        for filepath in self.playbooks_dir.glob("*.yaml"):
            try:
                with open(filepath, 'r') as f:
                    data = yaml.safe_load(f)
                
                # Convert to Playbook object
                steps = [
                    PlaybookStep(
                        name=step.get("name", f"Step {i+1}"),
                        description=step.get("description", ""),
                        command=step.get("command", ""),
                        expected_output=step.get("expected_output"),
                        timeout=step.get("timeout", 30),
                        continue_on_error=step.get("continue_on_error", False)
                    )
                    for i, step in enumerate(data.get("steps", []))
                ]
                
                playbook = Playbook(
                    id=data.get("id", filepath.stem),
                    name=data.get("name", filepath.stem),
                    description=data.get("description", ""),
                    steps=steps,
                    tags=data.get("tags", []),
                    created_at=datetime.fromisoformat(data.get("created_at")) if data.get("created_at") else None,
                    updated_at=datetime.fromisoformat(data.get("updated_at")) if data.get("updated_at") else None
                )
                
                self.playbooks[playbook.id] = playbook
            except Exception as e:
                print(f"Error loading playbook from {filepath}: {e}")
    
    def create_playbook(self, name: str, description: str, steps: List[Dict[str, Any]], 
                       tags: List[str] = None) -> Playbook:
        """Create a new playbook.
        
        Args:
            name: Name of the playbook
            description: Description of the playbook
            steps: List of steps
            tags: Tags for the playbook
            
        Returns:
            Created playbook
        """
        import uuid
        playbook_id = str(uuid.uuid4())
        
        # Convert steps to PlaybookStep objects
        playbook_steps = [
            PlaybookStep(
                name=step.get("name", f"Step {i+1}"),
                description=step.get("description", ""),
                command=step.get("command", ""),
                expected_output=step.get("expected_output"),
                timeout=step.get("timeout", 30),
                continue_on_error=step.get("continue_on_error", False)
            )
            for i, step in enumerate(steps)
        ]
        
        playbook = Playbook(
            id=playbook_id,
            name=name,
            description=description,
            steps=playbook_steps,
            tags=tags or []
        )
        
        self.playbooks[playbook_id] = playbook
        self._save_playbook(playbook)
        
        return playbook
    
    def _save_playbook(self, playbook: Playbook):
        """Save a playbook to a YAML file."""
        data = {
            "id": playbook.id,
            "name": playbook.name,
            "description": playbook.description,
            "steps": [
                {
                    "name": step.name,
                    "description": step.description,
                    "command": step.command,
                    "expected_output": step.expected_output,
                    "timeout": step.timeout,
                    "continue_on_error": step.continue_on_error
                }
                for step in playbook.steps
            ],
            "tags": playbook.tags,
            "created_at": playbook.created_at.isoformat(),
            "updated_at": playbook.updated_at.isoformat()
        }
        
        filepath = self.playbooks_dir / f"{playbook.id}.yaml"
        with open(filepath, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    
    def get_playbook(self, playbook_id: str) -> Optional[Playbook]:
        """Get a playbook by ID.
        
        Args:
            playbook_id: ID of the playbook
            
        Returns:
            Playbook or None if not found
        """
        return self.playbooks.get(playbook_id)
    
    def list_playbooks(self) -> List[Dict[str, Any]]:
        """List all playbooks.
        
        Returns:
            List of playbook information
        """
        return [
            {
                "id": playbook.id,
                "name": playbook.name,
                "description": playbook.description,
                "step_count": len(playbook.steps),
                "tags": playbook.tags,
                "created_at": playbook.created_at.isoformat() if playbook.created_at else None
            }
            for playbook in self.playbooks.values()
        ]
    
    def search_playbooks(self, query: str) -> List[Dict[str, Any]]:
        """Search playbooks by query.
        
        Args:
            query: Search query
            
        Returns:
            List of matching playbooks
        """
        query_lower = query.lower()
        results = []
        
        for playbook in self.playbooks.values():
            # Match by name, description, or tags
            if (query_lower in playbook.name.lower() or 
                query_lower in playbook.description.lower() or
                any(query_lower in tag.lower() for tag in playbook.tags)):
                results.append({
                    "id": playbook.id,
                    "name": playbook.name,
                    "description": playbook.description,
                    "step_count": len(playbook.steps),
                    "tags": playbook.tags,
                    "created_at": playbook.created_at.isoformat() if playbook.created_at else None
                })
        
        return results
    
    def delete_playbook(self, playbook_id: str) -> bool:
        """Delete a playbook.
        
        Args:
            playbook_id: ID of the playbook to delete
            
        Returns:
            True if deleted, False if not found
        """
        if playbook_id in self.playbooks:
            playbook = self.playbooks[playbook_id]
            filepath = self.playbooks_dir / f"{playbook_id}.yaml"
            if filepath.exists():
                filepath.unlink()
            del self.playbooks[playbook_id]
            return True
        return False
    
    def update_playbook(self, playbook_id: str, **kwargs) -> Optional[Playbook]:
        """Update a playbook.
        
        Args:
            playbook_id: ID of the playbook to update
            **kwargs: Fields to update
            
        Returns:
            Updated playbook or None if not found
        """
        if playbook_id not in self.playbooks:
            return None
        
        playbook = self.playbooks[playbook_id]
        
        # Update fields
        if "name" in kwargs:
            playbook.name = kwargs["name"]
        if "description" in kwargs:
            playbook.description = kwargs["description"]
        if "steps" in kwargs:
            # Convert steps to PlaybookStep objects
            steps = kwargs["steps"]
            playbook_steps = [
                PlaybookStep(
                    name=step.get("name", f"Step {i+1}"),
                    description=step.get("description", ""),
                    command=step.get("command", ""),
                    expected_output=step.get("expected_output"),
                    timeout=step.get("timeout", 30),
                    continue_on_error=step.get("continue_on_error", False)
                )
                for i, step in enumerate(steps)
            ]
            playbook.steps = playbook_steps
        if "tags" in kwargs:
            playbook.tags = kwargs["tags"]
        
        # Update timestamp
        playbook.updated_at = datetime.now()
        
        # Save updated playbook
        self._save_playbook(playbook)
        
        return playbook
    
    def execute_playbook(self, playbook_id: str, dry_run: bool = False) -> Dict[str, Any]:
        """Execute a playbook.
        
        Args:
            playbook_id: ID of the playbook to execute
            dry_run: If True, only show what would be executed without actually running
            
        Returns:
            Execution result
        """
        if playbook_id not in self.playbooks:
            raise ValueError(f"Playbook with ID {playbook_id} not found")
        
        playbook = self.playbooks[playbook_id]
        result = {
            "playbook_id": playbook_id,
            "playbook_name": playbook.name,
            "status": "started",
            "start_time": datetime.now().isoformat(),
            "steps": [],
            "end_time": None,
            "error": None
        }
        
        if dry_run:
            result["status"] = "dry_run"
            result["steps"] = [
                {
                    "step": i + 1,
                    "name": step.name,
                    "description": step.description,
                    "command": step.command,
                    "status": "would_execute"
                }
                for i, step in enumerate(playbook.steps)
            ]
            result["end_time"] = datetime.now().isoformat()
            return result
        
        # Execute each step
        for i, step in enumerate(playbook.steps):
            step_result = {
                "step": i + 1,
                "name": step.name,
                "description": step.description,
                "command": step.command,
                "status": "pending",
                "start_time": None,
                "end_time": None,
                "output": None,
                "error": None
            }
            
            result["steps"].append(step_result)
            
            try:
                step_result["start_time"] = datetime.now().isoformat()
                step_result["status"] = "running"
                
                # In a real implementation, you would execute the command here
                # For now, we'll simulate execution
                import subprocess
                import time
                
                # Simulate command execution
                time.sleep(0.1)  # Small delay to simulate execution
                
                # For demonstration, we'll just echo the command
                process = subprocess.Popen(
                    ["echo", f"Executing: {step.command}"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = process.communicate(timeout=step.timeout)
                
                step_result["status"] = "completed"
                step_result["output"] = stdout
                step_result["end_time"] = datetime.now().isoformat()
                
            except subprocess.TimeoutExpired:
                step_result["status"] = "timeout"
                step_result["error"] = f"Step timed out after {step.timeout} seconds"
                step_result["end_time"] = datetime.now().isoformat()
                
                if not step.continue_on_error:
                    result["status"] = "failed"
                    result["error"] = f"Step {i+1} timed out"
                    result["end_time"] = datetime.now().isoformat()
                    return result
                    
            except Exception as e:
                step_result["status"] = "error"
                step_result["error"] = str(e)
                step_result["end_time"] = datetime.now().isoformat()
                
                if not step.continue_on_error:
                    result["status"] = "failed"
                    result["error"] = f"Step {i+1} failed: {str(e)}"
                    result["end_time"] = datetime.now().isoformat()
                    return result
        
        result["status"] = "completed"
        result["end_time"] = datetime.now().isoformat()
        return result