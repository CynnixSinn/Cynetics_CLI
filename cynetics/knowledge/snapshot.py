import json
import os
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

class KnowledgeSnapshot:
    """A system for saving and reloading state/context across sessions."""
    
    def __init__(self, snapshot_dir: str = "snapshots"):
        self.snapshot_dir = Path(snapshot_dir)
        self.snapshot_dir.mkdir(exist_ok=True)
    
    def save_snapshot(self, name: str, data: Dict[str, Any]) -> str:
        """Save a knowledge snapshot.
        
        Args:
            name: Name of the snapshot
            data: Data to save in the snapshot
            
        Returns:
            Path to the saved snapshot file
        """
        # Add metadata
        snapshot_data = {
            "name": name,
            "created_at": datetime.now().isoformat(),
            "data": data
        }
        
        # Create filename
        filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.snapshot_dir / filename
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(snapshot_data, f, indent=2)
        
        return str(filepath)
    
    def load_snapshot(self, name: str) -> Dict[str, Any]:
        """Load a knowledge snapshot by name.
        
        Args:
            name: Name of the snapshot to load
            
        Returns:
            Snapshot data
        """
        # Find the latest snapshot with the given name
        snapshots = list(self.snapshot_dir.glob(f"{name}_*.json"))
        if not snapshots:
            raise FileNotFoundError(f"No snapshot found with name: {name}")
        
        # Sort by modification time (newest first)
        snapshots.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Load the most recent snapshot
        with open(snapshots[0], 'r') as f:
            return json.load(f)
    
    def list_snapshots(self) -> List[Dict[str, Any]]:
        """List all available snapshots.
        
        Returns:
            List of snapshot metadata
        """
        snapshots = []
        for filepath in self.snapshot_dir.glob("*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    snapshots.append({
                        "name": data.get("name"),
                        "created_at": data.get("created_at"),
                        "filepath": str(filepath)
                    })
            except Exception:
                # Skip corrupted files
                pass
        
        # Sort by creation time (newest first)
        snapshots.sort(key=lambda x: x["created_at"], reverse=True)
        return snapshots
    
    def delete_snapshot(self, name: str) -> bool:
        """Delete a snapshot by name.
        
        Args:
            name: Name of the snapshot to delete
            
        Returns:
            True if deleted, False if not found
        """
        try:
            snapshot = self.load_snapshot(name)
            filepath = snapshot.get("filepath")
            if filepath:
                os.remove(filepath)
                return True
        except FileNotFoundError:
            pass
        
        return False
    
    def save_conversation_history(self, name: str, history: List[Dict[str, Any]]) -> str:
        """Save conversation history as a snapshot.
        
        Args:
            name: Name of the snapshot
            history: Conversation history to save
            
        Returns:
            Path to the saved snapshot file
        """
        data = {
            "type": "conversation_history",
            "history": history
        }
        return self.save_snapshot(name, data)
    
    def load_conversation_history(self, name: str) -> List[Dict[str, Any]]:
        """Load conversation history from a snapshot.
        
        Args:
            name: Name of the snapshot to load
            
        Returns:
            Conversation history
        """
        snapshot = self.load_snapshot(name)
        data = snapshot.get("data", {})
        if data.get("type") == "conversation_history":
            return data.get("history", [])
        else:
            raise ValueError(f"Snapshot '{name}' is not a conversation history")
    
    def save_context(self, name: str, context: Dict[str, Any]) -> str:
        """Save context as a snapshot.
        
        Args:
            name: Name of the snapshot
            context: Context to save
            
        Returns:
            Path to the saved snapshot file
        """
        data = {
            "type": "context",
            "context": context
        }
        return self.save_snapshot(name, data)
    
    def load_context(self, name: str) -> Dict[str, Any]:
        """Load context from a snapshot.
        
        Args:
            name: Name of the snapshot to load
            
        Returns:
            Context data
        """
        snapshot = self.load_snapshot(name)
        data = snapshot.get("data", {})
        if data.get("type") == "context":
            return data.get("context", {})
        else:
            raise ValueError(f"Snapshot '{name}' is not a context snapshot")