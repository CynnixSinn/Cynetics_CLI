from typing import Dict, Any, List
from cynetics.protocols.base import ProtocolHandler
import subprocess
import os

class GitProtocolHandler(ProtocolHandler):
    \"\"\"Git protocol handler.\"\"\"
    
    def __init__(self):
        super().__init__(\"git\")
        self.connected = False
        self.repo_path = None
    
    def connect(self, config: Dict[str, Any]) -> bool:
        \"\"\"Connect to Git repository.\"\"\"
        self.repo_path = config.get(\"repo_path\", \".\")
        
        # Check if the path exists and is a Git repository
        if not os.path.exists(self.repo_path):
            return False
        
        # Check if it's a Git repository
        git_dir = os.path.join(self.repo_path, \".git\")
        if not os.path.exists(git_dir):
            return False
        
        self.connected = True
        return True
    
    def disconnect(self):
        \"\"\"Disconnect from Git repository.\"\"\"
        self.connected = False
        self.repo_path = None
    
    def execute_action(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        \"\"\"Execute a Git action.\"\"\"
        if not self.connected:
            return {\"error\": \"Not connected to Git repository\"}
        
        # Change to the repository directory
        original_cwd = os.getcwd()
        try:
            os.chdir(self.repo_path)
            
            if action == \"status\":
                result = subprocess.run(
                    [\"git\", \"status\", \"--porcelain\"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    # Parse the status output
                    changes = []
                    for line in result.stdout.strip().split('\n'):
                        if line:
                            status, file_path = line.split(maxsplit=1)
                            changes.append({\"status\": status, \"file\": file_path})
                    
                    return {\"changes\": changes}
                else:
                    return {\"error\": result.stderr}
            
            elif action == \"log\":
                limit = params.get(\"limit\", 10)
                result = subprocess.run(
                    [\"git\", \"log\", f\"--oneline\", f\"-n\", str(limit)],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    commits = []
                    for line in result.stdout.strip().split('\n'):
                        if line:
                            commit_hash, message = line.split(' ', 1)
                            commits.append({\"hash\": commit_hash, \"message\": message})
                    
                    return {\"commits\": commits}
                else:
                    return {\"error\": result.stderr}
            
            elif action == \"commit\":
                message = params.get(\"message\")
                if not message:
                    return {\"error\": \"Missing 'message' parameter\"}
                
                # Add all changes
                subprocess.run([\"git\", \"add\", \".\"], capture_output=True)
                
                # Commit changes
                result = subprocess.run(
                    [\"git\", \"commit\", \"-m\", message],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    return {\"message\": \"Changes committed successfully\"}
                else:
                    return {\"error\": result.stderr}
            
            elif action == \"push\":
                remote = params.get(\"remote\", \"origin\")
                branch = params.get(\"branch\", \"main\")
                
                result = subprocess.run(
                    [\"git\", \"push\", remote, branch],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    return {\"message\": f\"Pushed to {remote}/{branch}\"}
                else:
                    return {\"error\": result.stderr}
            
            elif action == \"pull\":
                remote = params.get(\"remote\", \"origin\")
                branch = params.get(\"branch\", \"main\")
                
                result = subprocess.run(
                    [\"git\", \"pull\", remote, branch],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    return {\"message\": f\"Pulled from {remote}/{branch}\"}
                else:
                    return {\"error\": result.stderr}
            
            else:
                return {\"error\": f\"Unknown action: {action}\"}
        
        finally:
            # Restore original working directory
            os.chdir(original_cwd)
    
    def list_actions(self) -> List[str]:
        \"\"\"List available Git actions.\"\"\"
        return [\"status\", \"log\", \"commit\", \"push\", \"pull\"]