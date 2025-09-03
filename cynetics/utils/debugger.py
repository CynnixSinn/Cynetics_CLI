import subprocess
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class DebugLevel(Enum):
    """Enumeration of debug levels."""
    BASIC = "basic"
    DETAILED = "detailed"
    VERBOSE = "verbose"

@dataclass
class DebugResult:
    """Result of a debug session."""
    command: str
    success: bool
    output: str
    error: str
    exit_code: Optional[int]
    analysis: Dict[str, Any]
    suggestions: List[str]

class ConversationalDebugger:
    """A conversational debugging system for CLI commands."""
    
    def __init__(self):
        self.debug_history = []
    
    def debug_command(self, command: str, debug_level: DebugLevel = DebugLevel.BASIC) -> DebugResult:
        """Debug a command conversationally.
        
        Args:
            command: Command to debug
            debug_level: Level of debugging detail
            
        Returns:
            Debug result with analysis and suggestions
        """
        # Execute the command
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()
            exit_code = process.returncode
            
            success = exit_code == 0
            output = stdout
            error = stderr
        except Exception as e:
            success = False
            output = ""
            error = str(e)
            exit_code = None
        
        # Analyze the result
        analysis = self._analyze_result(command, success, output, error, exit_code, debug_level)
        suggestions = self._generate_suggestions(command, success, output, error, exit_code, analysis)
        
        # Create debug result
        result = DebugResult(
            command=command,
            success=success,
            output=output,
            error=error,
            exit_code=exit_code,
            analysis=analysis,
            suggestions=suggestions
        )
        
        # Store in history
        self.debug_history.append(result)
        
        return result
    
    def _analyze_result(self, command: str, success: bool, output: str, error: str, 
                       exit_code: Optional[int], debug_level: DebugLevel) -> Dict[str, Any]:
        """Analyze the command execution result.
        
        Args:
            command: Executed command
            success: Whether the command succeeded
            output: Command stdout
            error: Command stderr
            exit_code: Exit code
            debug_level: Debug level
            
        Returns:
            Analysis dictionary
        """
        analysis = {
            "command": command,
            "success": success,
            "exit_code": exit_code
        }
        
        if debug_level == DebugLevel.BASIC:
            # Basic analysis
            if not success:
                if "command not found" in error:
                    analysis["issue"] = "command_not_found"
                    analysis["description"] = "The command was not found in your system PATH"
                elif "Permission denied" in error:
                    analysis["issue"] = "permission_denied"
                    analysis["description"] = "You don't have permission to execute this command"
                elif "No such file or directory" in error:
                    analysis["issue"] = "file_not_found"
                    analysis["description"] = "A file or directory referenced in the command was not found"
                else:
                    analysis["issue"] = "unknown_error"
                    analysis["description"] = "An unknown error occurred"
            else:
                analysis["issue"] = "none"
                analysis["description"] = "The command executed successfully"
        
        elif debug_level == DebugLevel.DETAILED:
            # Detailed analysis
            analysis.update(self._basic_analysis(success, error))
            
            # Look for specific error patterns
            if not success:
                # Check for missing dependencies
                if "import" in command and "ModuleNotFoundError" in error:
                    module_match = re.search(r"No module named '([^']+)'", error)
                    if module_match:
                        analysis["missing_module"] = module_match.group(1)
                
                # Check for file permissions
                if "Permission denied" in error:
                    file_match = re.search(r"Permission denied.*'([^']+)'", error)
                    if file_match:
                        analysis["problematic_file"] = file_match.group(1)
                
                # Check for syntax errors
                if "SyntaxError" in error:
                    analysis["syntax_error"] = True
                
                # Check for network issues
                if "Connection refused" in error or "Network is unreachable" in error:
                    analysis["network_issue"] = True
        
        elif debug_level == DebugLevel.VERBOSE:
            # Verbose analysis
            analysis.update(self._basic_analysis(success, error))
            analysis["stdout_length"] = len(output)
            analysis["stderr_length"] = len(error)
            
            # Count lines in output
            analysis["stdout_lines"] = len(output.split('\n')) if output else 0
            analysis["stderr_lines"] = len(error.split('\n')) if error else 0
            
            # Look for common keywords in output
            keywords = ["error", "warning", "failed", "success", "completed"]
            found_keywords = []
            for keyword in keywords:
                if keyword in output.lower() or keyword in error.lower():
                    found_keywords.append(keyword)
            analysis["keywords"] = found_keywords
        
        return analysis
    
    def _basic_analysis(self, success: bool, error: str) -> Dict[str, Any]:
        """Perform basic error analysis.
        
        Args:
            success: Whether the command succeeded
            error: Command stderr
            
        Returns:
            Basic analysis dictionary
        """
        analysis = {"success": success}
        
        if not success:
            if "command not found" in error:
                analysis["issue"] = "command_not_found"
                analysis["description"] = "The command was not found in your system PATH"
            elif "Permission denied" in error:
                analysis["issue"] = "permission_denied"
                analysis["description"] = "You don't have permission to execute this command"
            elif "No such file or directory" in error:
                analysis["issue"] = "file_not_found"
                analysis["description"] = "A file or directory referenced in the command was not found"
            elif "SyntaxError" in error:
                analysis["issue"] = "syntax_error"
                analysis["description"] = "There is a syntax error in the command"
            elif "ImportError" in error or "ModuleNotFoundError" in error:
                analysis["issue"] = "import_error"
                analysis["description"] = "A required module or library is missing"
            elif "Connection refused" in error or "Network is unreachable" in error:
                analysis["issue"] = "network_error"
                analysis["description"] = "There is a network connectivity issue"
            else:
                analysis["issue"] = "unknown_error"
                analysis["description"] = "An unknown error occurred"
        else:
            analysis["issue"] = "none"
            analysis["description"] = "The command executed successfully"
        
        return analysis
    
    def _generate_suggestions(self, command: str, success: bool, output: str, error: str, 
                             exit_code: Optional[int], analysis: Dict[str, Any]) -> List[str]:
        """Generate suggestions for fixing issues.
        
        Args:
            command: Executed command
            success: Whether the command succeeded
            output: Command stdout
            error: Command stderr
            exit_code: Exit code
            analysis: Analysis dictionary
            
        Returns:
            List of suggestions
        """
        suggestions = []
        
        if success:
            suggestions.append("The command executed successfully. No action needed.")
            return suggestions
        
        issue = analysis.get("issue", "unknown_error")
        
        if issue == "command_not_found":
            suggestions.append("Check that the command is installed and in your PATH")
            suggestions.append("Try installing the package that provides this command")
            suggestions.append("Use 'which <command>' to check if it's available")
        
        elif issue == "permission_denied":
            suggestions.append("Check file permissions with 'ls -l <file>'")
            suggestions.append("Try running with sudo if appropriate: 'sudo " + command + "'")
            suggestions.append("Check if you have the necessary privileges to execute this command")
        
        elif issue == "file_not_found":
            suggestions.append("Verify that all file paths in the command are correct")
            suggestions.append("Check that the files exist with 'ls <path>'")
            suggestions.append("Make sure you're in the correct directory")
        
        elif issue == "syntax_error":
            suggestions.append("Check the command syntax for errors")
            suggestions.append("Refer to the command's manual with 'man <command>'")
            suggestions.append("Try breaking the command into smaller parts to isolate the issue")
        
        elif issue == "import_error":
            missing_module = analysis.get("missing_module")
            if missing_module:
                suggestions.append(f"Install the missing module: 'pip install {missing_module}'")
            else:
                suggestions.append("Install the required Python modules")
            suggestions.append("Check your Python environment and virtual environment")
        
        elif issue == "network_error":
            suggestions.append("Check your network connection")
            suggestions.append("Verify that the remote server is accessible")
            suggestions.append("Check firewall settings if applicable")
        
        else:
            # Generic suggestions
            suggestions.append("Check the error message for specific details")
            suggestions.append("Try running the command with verbose output if available")
            suggestions.append("Consult the command's documentation or manual")
            suggestions.append("Search online for the specific error message")
        
        return suggestions
    
    def explain_error(self, error: str) -> str:
        """Provide a conversational explanation of an error.
        
        Args:
            error: Error message to explain
            
        Returns:
            Explanation of the error
        """
        if "command not found" in error:
            return ("It looks like the command you're trying to run isn't installed on your system, "
                   "or it's not in your PATH. This means your system doesn't know where to find the "
                   "program you're trying to execute.")
        
        elif "Permission denied" in error:
            return ("You don't have the necessary permissions to execute this command or access "
                   "the file/directory it's trying to work with. This is a security feature to "
                   "prevent unauthorized access to system resources.")
        
        elif "No such file or directory" in error:
            return ("The command is trying to access a file or directory that doesn't exist at the "
                   "specified path. This could be because the path is incorrect, the file was moved "
                   "or deleted, or you're in the wrong directory.")
        
        elif "SyntaxError" in error:
            return ("There's an error in the syntax of your command, likely in a script or programming "
                   "language you're using. This means there's a mistake in how the command is written, "
                   "such as a missing parenthesis, quote, or incorrect indentation.")
        
        elif "ImportError" in error or "ModuleNotFoundError" in error:
            return ("A Python module or library that your command depends on is missing. This usually "
                   "happens when required packages haven't been installed in your Python environment.")
        
        elif "Connection refused" in error or "Network is unreachable" in error:
            return ("Your command is trying to connect to a network service, but the connection is "
                   "failing. This could be because the service is down, there's a network issue, "
                   "or a firewall is blocking the connection.")
        
        else:
            return ("I'm not familiar with this specific error, but I can see something went wrong "
                   "when executing your command. The error message should give you more details about "
                   "what happened. Try searching online for the exact error message to find solutions.")
    
    def get_debug_history(self) -> List[DebugResult]:
        """Get the debug history.
        
        Returns:
            List of debug results
        """
        return self.debug_history.copy()
    
    def clear_debug_history(self):
        """Clear the debug history."""
        self.debug_history.clear()