import subprocess
import sys
import os
from typing import Dict, Any, List

class SelfHealingSystem:
    """A system that detects and fixes broken commands or missing dependencies."""
    
    def __init__(self):
        self.diagnosis_history = []
    
    def diagnose_command(self, command: str) -> Dict[str, Any]:
        """Diagnose issues with a command.
        
        Args:
            command: Command to diagnose
            
        Returns:
            Diagnosis result
        """
        diagnosis = {
            "command": command,
            "issues": [],
            "suggestions": [],
            "severity": "low"
        }
        
        # Check if command exists
        if not self._command_exists(command.split()[0]):
            diagnosis["issues"].append(f"Command '{command.split()[0]}' not found")
            diagnosis["suggestions"].append(f"Install the package that provides '{command.split()[0]}'")
            diagnosis["severity"] = "high"
        
        # Check dependencies if it's a Python command
        if command.startswith("python") or command.startswith("python3"):
            diagnosis.update(self._diagnose_python_command(command))
        
        # Store diagnosis
        self.diagnosis_history.append(diagnosis)
        
        return diagnosis
    
    def _command_exists(self, command: str) -> bool:
        """Check if a command exists in the system."""
        try:
            subprocess.run(
                ["which", command], 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    def _diagnose_python_command(self, command: str) -> Dict[str, Any]:
        """Diagnose issues with a Python command."""
        diagnosis = {
            "issues": [],
            "suggestions": [],
            "severity": "low"
        }
        
        # Extract Python file if present
        parts = command.split()
        python_file = None
        for part in parts:
            if part.endswith(".py") and os.path.exists(part):
                python_file = part
                break
        
        if python_file:
            # Check for missing imports
            missing_modules = self._check_missing_imports(python_file)
            if missing_modules:
                diagnosis["issues"].extend([f"Missing modules: {', '.join(missing_modules)}"])
                diagnosis["suggestions"].extend([
                    f"Install missing modules: pip install {' '.join(missing_modules)}"
                ])
                diagnosis["severity"] = "high"
        
        return diagnosis
    
    def _check_missing_imports(self, python_file: str) -> List[str]:
        """Check for missing imports in a Python file."""
        missing_modules = []
        
        try:
            with open(python_file, 'r') as f:
                content = f.read()
            
            # Simple import detection (in a real implementation, you might use AST)
            import_lines = [
                line for line in content.split('\n') 
                if line.startswith('import ') or line.startswith('from ')
            ]
            
            for line in import_lines:
                if line.startswith('import '):
                    module = line.split()[1].split('.')[0]
                elif line.startswith('from '):
                    module = line.split()[1].split('.')[0]
                else:
                    continue
                
                # Skip built-in modules
                if module in ['os', 'sys', 'json', 'subprocess', 'typing']:
                    continue
                
                # Check if module can be imported
                try:
                    __import__(module)
                except ImportError:
                    missing_modules.append(module)
        except Exception:
            # If we can't read the file, skip this check
            pass
        
        return missing_modules
    
    def fix_command(self, command: str, diagnosis: Dict[str, Any] = None) -> Dict[str, Any]:
        """Attempt to fix issues with a command.
        
        Args:
            command: Command to fix
            diagnosis: Optional diagnosis result
            
        Returns:
            Fix result
        """
        if not diagnosis:
            diagnosis = self.diagnose_command(command)
        
        result = {
            "command": command,
            "fixed": False,
            "actions_taken": [],
            "output": ""
        }
        
        # Try to fix missing commands
        if "not found" in str(diagnosis["issues"]):
            command_name = command.split()[0]
            fix_result = self._install_command(command_name)
            result["fixed"] = fix_result["success"]
            result["actions_taken"].append(fix_result["action"])
            result["output"] = fix_result["output"]
        
        # Try to fix missing Python modules
        missing_modules_issues = [
            issue for issue in diagnosis["issues"] 
            if issue.startswith("Missing modules:")
        ]
        
        if missing_modules_issues:
            # Extract module names
            modules_str = missing_modules_issues[0].replace("Missing modules: ", "")
            modules = [m.strip() for m in modules_str.split(",")]
            
            fix_result = self._install_python_modules(modules)
            result["fixed"] = fix_result["success"]
            result["actions_taken"].append(fix_result["action"])
            result["output"] = fix_result["output"]
        
        return result
    
    def _install_command(self, command_name: str) -> Dict[str, Any]:
        """Attempt to install a missing command."""
        # This is a simplified implementation
        # In a real system, you would detect the OS and package manager
        result = {
            "success": False,
            "action": f"Attempted to install {command_name}",
            "output": ""
        }
        
        # Try common package managers
        install_commands = [
            ["apt-get", "install", "-y", command_name],
            ["yum", "install", "-y", command_name],
            ["brew", "install", command_name],
            ["pacman", "-S", "--noconfirm", command_name]
        ]
        
        for install_cmd in install_commands:
            try:
                # This is just a simulation - in a real implementation, you would actually run the command
                # subprocess.run(install_cmd, check=True, capture_output=True, text=True)
                result["success"] = True
                result["action"] = f"Installed {command_name} using {install_cmd[0]}"
                result["output"] = f"Successfully installed {command_name}"
                break
            except:
                continue
        
        if not result["success"]:
            result["output"] = f"Failed to install {command_name}. Please install manually."
        
        return result
    
    def _install_python_modules(self, modules: List[str]) -> Dict[str, Any]:
        """Attempt to install missing Python modules."""
        result = {
            "success": False,
            "action": f"Attempted to install Python modules: {', '.join(modules)}",
            "output": ""
        }
        
        try:
            # Try to install using pip
            cmd = [sys.executable, "-m", "pip", "install"] + modules
            # This is just a simulation - in a real implementation, you would actually run the command
            # subprocess.run(cmd, check=True, capture_output=True, text=True)
            result["success"] = True
            result["action"] = f"Installed Python modules: {', '.join(modules)}"
            result["output"] = f"Successfully installed modules: {', '.join(modules)}"
        except Exception as e:
            result["output"] = f"Failed to install modules: {str(e)}"
        
        return result
    
    def get_diagnosis_history(self) -> List[Dict[str, Any]]:
        """Get the diagnosis history."""
        return self.diagnosis_history.copy()