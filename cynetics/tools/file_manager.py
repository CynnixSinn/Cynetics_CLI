import os
from cynetics.tools.base import BaseTool

class FileManagerTool(BaseTool):
    """A simple file management tool."""
    
    def __init__(self):
        super().__init__(
            name="file_manager",
            description="Perform basic file operations like listing, reading, and writing files."
        )

    def run(self, action: str, path: str = None, content: str = None) -> dict:
        """Execute a file operation.
        
        Args:
            action: The action to perform (list, read, write).
            path: The file or directory path.
            content: Content to write (for write action).
            
        Returns:
            A dictionary with the result of the operation.
        """
        try:
            if action == "list":
                if path is None:
                    path = "."
                items = os.listdir(path)
                return {
                    "status": "success",
                    "action": "list",
                    "path": path,
                    "items": items
                }
            elif action == "read":
                if path is None:
                    return {"status": "error", "message": "Path is required for read action."}
                with open(path, 'r') as f:
                    content = f.read()
                return {
                    "status": "success",
                    "action": "read",
                    "path": path,
                    "content": content
                }
            elif action == "write":
                if path is None or content is None:
                    return {"status": "error", "message": "Path and content are required for write action."}
                with open(path, 'w') as f:
                    f.write(content)
                return {
                    "status": "success",
                    "action": "write",
                    "path": path,
                    "message": f"Content written to {path}"
                }
            else:
                return {"status": "error", "message": f"Unknown action: {action}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}