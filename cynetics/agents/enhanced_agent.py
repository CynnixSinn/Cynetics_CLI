from typing import Dict, Any, List
from cynetics.tools import load_tool

class EnhancedAgent:
    """An enhanced agent with multi-step reasoning and tool chaining capabilities."""
    
    def __init__(self, tool_names: list):
        self.tools = {}
        self.context = {}  # Context storage for multi-step reasoning
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
    
    def update_context(self, key: str, value: Any):
        """Update the agent's context with a key-value pair."""
        self.context[key] = value
    
    def get_context(self, key: str) -> Any:
        """Retrieve a value from the agent's context."""
        return self.context.get(key)
    
    def execute_tool_chain(self, tool_chain: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute a chain of tool commands.
        
        Args:
            tool_chain: A list of dictionaries, each containing 'tool' and 'args' keys.
            
        Returns:
            A list of results from each tool execution.
        """
        results = []
        for step in tool_chain:
            tool_name = step.get("tool")
            args = step.get("args", {})
            
            # Merge context into args if specified
            if "use_context" in step:
                for ctx_key in step["use_context"]:
                    if ctx_key in self.context:
                        args[ctx_key] = self.context[ctx_key]
            
            result = self.execute_tool(tool_name, **args)
            results.append(result)
            
            # Store result in context if specified
            if "store_result" in step:
                self.context[step["store_result"]] = result
                
        return results