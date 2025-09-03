from typing import Dict, Any
from cynetics.tools import load_tool

class SimpleAgent:
    """A simple agent that can execute tool commands."""
    
    def __init__(self, tool_names: list):
        self.tools = {}
        for name in tool_names:
            try:
                self.tools[name] = load_tool(name)
            except ValueError as e:
                print(f"Warning: {e}")
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool by name with given arguments."""
        if tool_name not in self.tools:
            return {"status": "error", "message": f"Tool '{tool_name}' not found."}
        
        try:
            return self.tools[tool_name].run(**kwargs)
        except Exception as e:
            return {"status": "error", "message": str(e)}