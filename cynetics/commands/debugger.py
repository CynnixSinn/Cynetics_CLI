import click
import json
import subprocess
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

class DebugManager:
    """Conversational debugging system."""
    
    def __init__(self, storage_dir: str = "debug_sessions"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.history_file = self.storage_dir / "debug_history.json"
        self._load_history()
    
    def _load_history(self):
        """Load debug history from file."""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = []
    
    def _save_history(self):
        """Save debug history to file."""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def debug_command(self, command: str) -> Dict[str, Any]:
        """Debug a command by executing it and analyzing the result."""
        from uuid import uuid4
        
        # Execute the command
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            debug_info = {
                "id": str(uuid4()),
                "command": command,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
                "executed_at": datetime.now().isoformat()
            }
        except subprocess.TimeoutExpired:
            debug_info = {
                "id": str(uuid4()),
                "command": command,
                "error": "Command timed out",
                "executed_at": datetime.now().isoformat()
            }
        except Exception as e:
            debug_info = {
                "id": str(uuid4()),
                "command": command,
                "error": str(e),
                "executed_at": datetime.now().isoformat()
            }
        
        # Add to history
        self.history.append(debug_info)
        self._save_history()
        
        return debug_info
    
    def explain_error(self, error_message: str) -> Dict[str, Any]:
        """Provide a plain English explanation of an error."""
        explanations = {
            "command not found": "The command you're trying to run doesn't exist or isn't in your PATH.",
            "permission denied": "You don't have the necessary permissions to perform this action.",
            "no such file or directory": "The file or directory you're trying to access doesn't exist.",
            "connection refused": "The service you're trying to connect to is not running or not accepting connections."
        }
        
        # Find the best matching explanation
        best_match = None
        best_score = 0
        
        for pattern, explanation in explanations.items():
            # Simple string matching for now
            if pattern in error_message.lower():
                score = len(pattern)
                if score > best_score:
                    best_match = explanation
                    best_score = score
        
        return {
            "error_message": error_message,
            "explanation": best_match or "I couldn't find a specific explanation for this error.",
            "analyzed_at": datetime.now().isoformat()
        }
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get debug history."""
        return self.history[-limit:] if self.history else []

@click.command()
@click.option('--debug', help='Debug a command')
@click.option('--explain', help='Explain an error message')
@click.option('--history', is_flag=True, help='Show debug history')
@click.option('--limit', default=10, help='Limit history results')
def debugger(debug, explain, history, limit):
    """Debug commands with conversational explanations."""
    manager = DebugManager()
    
    if debug:
        try:
            result = manager.debug_command(debug)
            
            click.echo(f"Debugging command: {result['command']}")
            click.echo(f"Executed at: {result['executed_at']}")
            
            if "error" in result:
                click.echo(f"Error: {result['error']}")
            else:
                click.echo(f"Return code: {result['returncode']}")
                click.echo(f"Success: {result['success']}")
                
                if result['stdout']:
                    click.echo(f"Output: {result['stdout']}")
                if result['stderr']:
                    click.echo(f"Errors: {result['stderr']}")
                
                # Provide basic analysis
                if not result['success']:
                    if "command not found" in result['stderr'].lower():
                        click.echo("\nAnalysis: The command was not found. Check that you've typed it correctly and that it's installed.")
                    elif "permission denied" in result['stderr'].lower():
                        click.echo("\nAnalysis: Permission denied. You may need to run this command with sudo or check file permissions.")
                    elif "no such file or directory" in result['stderr'].lower():
                        click.echo("\nAnalysis: File or directory not found. Check the path and make sure it exists.")
                    else:
                        click.echo("\nAnalysis: The command failed. Check the error output above for details.")
        except Exception as e:
            click.echo(f"Error debugging command: {e}")
    
    elif explain:
        explanation = manager.explain_error(explain)
        click.echo(f"Error: {explanation['error_message']}")
        click.echo(f"Explanation: {explanation['explanation']}")
    
    elif history:
        history_data = manager.get_history(limit)
        if not history_data:
            click.echo("No debug history found.")
            return
        
        click.echo(f"Debug History (last {min(limit, len(history_data))} entries):")
        for entry in history_data:
            status_icon = "●" if entry.get("success", False) else "✗"
            click.echo(f"  {status_icon} {entry['command']}")
            click.echo(f"    Executed: {entry['executed_at']}")
            if "error" in entry:
                click.echo(f"    Error: {entry['error']}")
            else:
                click.echo(f"    Return code: {entry['returncode']}")
            click.echo()
    
    else:
        click.echo("Conversational Debugging System")
        click.echo("Use --debug to debug a command, --explain to explain an error, or --history to see debug history.")

if __name__ == "__main__":
    debugger()