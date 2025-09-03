import click
import json
import subprocess
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

class SelfHealingSystem:
    """Self-healing error system."""
    
    def __init__(self, storage_dir: str = "healing_sessions"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.history_file = self.storage_dir / "healing_history.json"
        self._load_history()
    
    def _load_history(self):
        """Load healing history from file."""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
        else:
            self.history = []
    
    def _save_history(self):
        """Save healing history to file."""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def diagnose_command(self, command: str) -> Dict[str, Any]:
        """Diagnose why a command is failing."""
        from uuid import uuid4
        
        # Execute the command to get the error
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            diagnosis = {
                "id": str(uuid4()),
                "command": command,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
                "diagnosed_at": datetime.now().isoformat()
            }
        except subprocess.TimeoutExpired:
            diagnosis = {
                "id": str(uuid4()),
                "command": command,
                "error": "Command timed out",
                "diagnosed_at": datetime.now().isoformat()
            }
        except Exception as e:
            diagnosis = {
                "id": str(uuid4()),
                "command": command,
                "error": str(e),
                "diagnosed_at": datetime.now().isoformat()
            }
        
        # Add diagnostic analysis
        diagnosis["analysis"] = self._analyze_result(diagnosis)
        
        # Add to history
        self.history.append(diagnosis)
        self._save_history()
        
        return diagnosis
    
    def _analyze_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze command result and provide suggestions."""
        analysis = {
            "issues": [],
            "suggestions": [],
            "dependencies": []
        }
        
        stderr = result.get("stderr", "").lower()
        stdout = result.get("stdout", "").lower()
        
        # Check for common issues
        if "command not found" in stderr or "command not found" in stdout:
            analysis["issues"].append("Command not found")
            analysis["suggestions"].append("Install the required package or check your PATH")
            # Try to identify the package
            cmd_parts = result["command"].split()
            if cmd_parts:
                cmd_name = cmd_parts[0]
                package = self._suggest_package(cmd_name)
                if package:
                    analysis["dependencies"].append(package)
        
        elif "permission denied" in stderr or "permission denied" in stdout:
            analysis["issues"].append("Permission denied")
            analysis["suggestions"].append("Run with sudo or check file permissions")
        
        elif "no such file or directory" in stderr or "no such file or directory" in stdout:
            analysis["issues"].append("File or directory not found")
            analysis["suggestions"].append("Check the file path and make sure it exists")
        
        elif "importerror" in stderr or "importerror" in stdout:
            analysis["issues"].append("Python import error")
            analysis["suggestions"].append("Install the required Python package")
            # Try to identify the package
            if "no module named" in stderr:
                parts = stderr.split("no module named")
                if len(parts) > 1:
                    module_name = parts[1].strip().split()[0].strip("'\"")
                    analysis["dependencies"].append(f"python:{module_name}")
        
        # If no specific issues found, provide general suggestions
        if not analysis["issues"]:
            analysis["issues"].append("Command failed")
            analysis["suggestions"].append("Check the command syntax and parameters")
        
        return analysis
    
    def _suggest_package(self, command: str) -> str:
        """Suggest a package for a missing command."""
        package_map = {
            "git": "git",
            "docker": "docker",
            "python3": "python3",
            "pip3": "python3-pip",
            "curl": "curl",
            "wget": "wget",
            "nano": "nano",
            "vim": "vim",
            "node": "nodejs",
            "npm": "npm",
            "java": "openjdk-11-jdk",
            "gcc": "gcc",
            "make": "make"
        }
        
        return package_map.get(command, f"{command} (package name may vary)")
    
    def fix_command(self, command: str) -> Dict[str, Any]:
        """Attempt to fix a command by installing dependencies."""
        from uuid import uuid4
        
        # First diagnose the command
        diagnosis = self.diagnose_command(command)
        
        # Try to fix based on diagnosis
        fixes = []
        
        for dependency in diagnosis["analysis"].get("dependencies", []):
            if dependency.startswith("python:"):
                # Python package
                package_name = dependency.split(":", 1)[1]
                try:
                    subprocess.run(["pip", "install", package_name], capture_output=True, timeout=60)
                    fixes.append(f"Installed Python package: {package_name}")
                except Exception as e:
                    fixes.append(f"Failed to install Python package {package_name}: {e}")
            else:
                # System package - this is more complex and platform-dependent
                fixes.append(f"Suggested package to install: {dependency} (install manually)")
        
        fix_result = {
            "id": str(uuid4()),
            "command": command,
            "diagnosis": diagnosis,
            "fixes_applied": fixes,
            "fixed_at": datetime.now().isoformat()
        }
        
        # Add to history
        self.history.append(fix_result)
        self._save_history()
        
        return fix_result
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get healing history."""
        return self.history[-limit:] if self.history else []

@click.command()
@click.option('--diagnose', help='Diagnose a command')
@click.option('--fix', help='Attempt to fix a command')
@click.option('--history', is_flag=True, help='Show diagnosis history')
@click.option('--limit', default=10, help='Limit history results')
def self_healing(diagnose, fix, history, limit):
    """Detect and fix broken commands or missing dependencies."""
    system = SelfHealingSystem()
    
    if diagnose:
        try:
            result = system.diagnose_command(diagnose)
            
            click.echo(f"Diagnosing command: {result['command']}")
            click.echo(f"Diagnosed at: {result['diagnosed_at']}")
            
            if "error" in result:
                click.echo(f"Error: {result['error']}")
            else:
                click.echo(f"Return code: {result['returncode']}")
                click.echo(f"Success: {result['success']}")
                
                if result['stdout']:
                    click.echo(f"Output: {result['stdout']}")
                if result['stderr']:
                    click.echo(f"Errors: {result['stderr']}")
                
                # Show analysis
                analysis = result['analysis']
                click.echo("\nAnalysis:")
                for issue in analysis['issues']:
                    click.echo(f"  Issue: {issue}")
                for suggestion in analysis['suggestions']:
                    click.echo(f"  Suggestion: {suggestion}")
                for dependency in analysis['dependencies']:
                    click.echo(f"  Dependency: {dependency}")
        except Exception as e:
            click.echo(f"Error diagnosing command: {e}")
    
    elif fix:
        try:
            result = system.fix_command(fix)
            
            click.echo(f"Attempting to fix command: {result['command']}")
            click.echo(f"Fixed at: {result['fixed_at']}")
            
            # Show diagnosis
            diagnosis = result['diagnosis']
            click.echo(f"\nDiagnosis:")
            if "error" in diagnosis:
                click.echo(f"  Error: {diagnosis['error']}")
            else:
                click.echo(f"  Return code: {diagnosis['returncode']}")
                click.echo(f"  Success: {diagnosis['success']}")
                
                if diagnosis['stderr']:
                    click.echo(f"  Errors: {diagnosis['stderr']}")
                
                # Show analysis
                analysis = diagnosis['analysis']
                click.echo(f"\nAnalysis:")
                for issue in analysis['issues']:
                    click.echo(f"  Issue: {issue}")
                for suggestion in analysis['suggestions']:
                    click.echo(f"  Suggestion: {suggestion}")
                for dependency in analysis['dependencies']:
                    click.echo(f"  Dependency: {dependency}")
            
            # Show fixes applied
            if result['fixes_applied']:
                click.echo(f"\nFixes applied:")
                for fix in result['fixes_applied']:
                    click.echo(f"  {fix}")
            else:
                click.echo(f"\nNo fixes were automatically applied.")
                click.echo("You may need to manually install dependencies.")
        except Exception as e:
            click.echo(f"Error fixing command: {e}")
    
    elif history:
        history_data = system.get_history(limit)
        if not history_data:
            click.echo("No healing history found.")
            return
        
        click.echo(f"Healing History (last {min(limit, len(history_data))} entries):")
        for entry in history_data:
            if "diagnosis" in entry:
                # Fix entry
                click.echo(f"  ⚡ Fix attempt for: {entry['command']}")
                click.echo(f"    Fixed at: {entry['fixed_at']}")
            else:
                # Diagnosis entry
                status_icon = "●" if entry.get("success", False) else "✗"
                click.echo(f"  {status_icon} Diagnosis for: {entry['command']}")
                click.echo(f"    Diagnosed at: {entry['diagnosed_at']}")
            
            if "error" in entry:
                click.echo(f"    Error: {entry['error']}")
            click.echo()
    
    else:
        click.echo("Self-Healing System")
        click.echo("Use --diagnose to analyze a command, --fix to attempt fixes, or --history to see healing history.")

if __name__ == "__main__":
    self_healing()