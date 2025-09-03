import click
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class KnowledgeSnapshotManager:
    """Manager for knowledge snapshots."""
    
    def __init__(self, storage_dir: str = "snapshots"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
    
    def save_snapshot(self, name: str, data_file: str) -> Dict[str, Any]:
        """Save a knowledge snapshot."""
        # Read the data from the file
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"Data file '{data_file}' not found")
        
        with open(data_file, 'r') as f:
            if data_file.endswith('.json'):
                data = json.load(f)
            else:
                data = f.read()
        
        # Create snapshot metadata
        snapshot = {
            "name": name,
            "data": data,
            "created_at": datetime.now().isoformat(),
            "data_file": data_file,
            "size": os.path.getsize(data_file)
        }
        
        # Save snapshot to file
        snapshot_file = self.storage_dir / f"{name}.json"
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        return snapshot
    
    def load_snapshot(self, name: str) -> Dict[str, Any]:
        """Load a knowledge snapshot."""
        snapshot_file = self.storage_dir / f"{name}.json"
        
        if not snapshot_file.exists():
            raise FileNotFoundError(f"Snapshot '{name}' not found")
        
        with open(snapshot_file, 'r') as f:
            snapshot = json.load(f)
        
        return snapshot
    
    def list_snapshots(self) -> Dict[str, Dict[str, Any]]:
        """List all snapshots."""
        snapshots = {}
        for snapshot_file in self.storage_dir.glob("*.json"):
            with open(snapshot_file, 'r') as f:
                snapshot = json.load(f)
                name = snapshot["name"]
                snapshots[name] = {
                    "created_at": snapshot["created_at"],
                    "data_file": snapshot["data_file"],
                    "size": snapshot["size"]
                }
        return snapshots
    
    def delete_snapshot(self, name: str) -> bool:
        """Delete a snapshot."""
        snapshot_file = self.storage_dir / f"{name}.json"
        
        if snapshot_file.exists():
            snapshot_file.unlink()
            return True
        return False

@click.command()
@click.option('--save', nargs=2, help='Save a snapshot (name data_file)')
@click.option('--load', help='Load a snapshot by name')
@click.option('--list', 'list_snapshots', is_flag=True, help='List all snapshots')
@click.option('--delete', help='Delete a snapshot by name')
def knowledge_snapshot(save, load, list_snapshots, delete):
    """Save and load state/context across sessions."""
    manager = KnowledgeSnapshotManager()
    
    if save:
        name, data_file = save
        try:
            snapshot = manager.save_snapshot(name, data_file)
            click.echo(f"Saved snapshot '{name}'")
            click.echo(f"  Data file: {snapshot['data_file']}")
            click.echo(f"  Size: {snapshot['size']} bytes")
            click.echo(f"  Created: {snapshot['created_at']}")
        except Exception as e:
            click.echo(f"Error saving snapshot: {e}")
    
    elif load:
        try:
            snapshot = manager.load_snapshot(load)
            click.echo(f"Loaded snapshot '{load}'")
            click.echo(f"  Data file: {snapshot['data_file']}")
            click.echo(f"  Size: {snapshot['size']} bytes")
            click.echo(f"  Created: {snapshot['created_at']}")
            
            # Save the data to a file
            output_file = f"restored_{load}.json"
            with open(output_file, 'w') as f:
                json.dump(snapshot['data'], f, indent=2)
            click.echo(f"  Data saved to: {output_file}")
        except Exception as e:
            click.echo(f"Error loading snapshot: {e}")
    
    elif list_snapshots:
        snapshots = manager.list_snapshots()
        if not snapshots:
            click.echo("No snapshots found.")
            return
        
        click.echo("Available snapshots:")
        for name, info in snapshots.items():
            click.echo(f"  {name}")
            click.echo(f"    Created: {info['created_at']}")
            click.echo(f"    Data file: {info['data_file']}")
            click.echo(f"    Size: {info['size']} bytes")
            click.echo()
    
    elif delete:
        if manager.delete_snapshot(delete):
            click.echo(f"Deleted snapshot '{delete}'")
        else:
            click.echo(f"Snapshot '{delete}' not found")
    
    else:
        click.echo("Knowledge Snapshot System")
        click.echo("Use --save to save a snapshot, --load to load a snapshot, --list to see all snapshots, or --delete to remove a snapshot.")

if __name__ == "__main__":
    knowledge_snapshot()