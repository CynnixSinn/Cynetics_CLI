from typing import Dict, Any, List, Callable
from cynetics.tools.base import BaseTool

class ToolChain:
    """A system for chaining multiple tools together."""
    
    def __init__(self):
        self.tools = {}
        self.chain_history = []
    
    def register_tool(self, name: str, tool: BaseTool):
        """Register a tool for use in chains."""
        self.tools[name] = tool
    
    def execute_chain(self, chain: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute a chain of tools.
        
        Args:
            chain: List of tool specifications, each with 'name' and 'args' keys
            
        Returns:
            Dictionary with results from each tool in the chain
        """
        results = {
            "chain_results": [],
            "final_output": None,
            "success": True,
            "errors": []
        }
        
        # Shared context between tools in the chain
        context = {}
        
        for i, step in enumerate(chain):
            tool_name = step.get("name")
            args = step.get("args", {})
            
            # Merge context with provided args
            merged_args = {**context, **args}
            
            if tool_name not in self.tools:
                error_msg = f"Tool '{tool_name}' not found in registry"
                results["errors"].append(error_msg)
                results["success"] = False
                continue
            
            try:
                tool = self.tools[tool_name]
                tool_result = tool.run(**merged_args)
                
                # Store result
                step_result = {
                    "step": i,
                    "tool": tool_name,
                    "args": merged_args,
                    "result": tool_result
                }
                results["chain_results"].append(step_result)
                
                # Update context with successful results
                if tool_result.get("status") == "success":
                    context[f"{tool_name}_result"] = tool_result
                    # If the tool provides a specific output field, use that
                    if "output" in tool_result:
                        context[f"{tool_name}_output"] = tool_result["output"]
                else:
                    results["errors"].append(f"Tool '{tool_name}' failed: {tool_result.get('message', 'Unknown error')}")
                    results["success"] = False
                    
            except Exception as e:
                error_msg = f"Error executing tool '{tool_name}': {str(e)}"
                results["errors"].append(error_msg)
                results["success"] = False
        
        # Set final output as the result of the last successful tool
        if results["chain_results"]:
            results["final_output"] = results["chain_results"][-1]["result"]
        
        # Store in history
        self.chain_history.append({
            "chain": chain,
            "results": results,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        })
        
        return results
    
    def create_chain_from_prompt(self, prompt: str, available_tools: List[str]) -> List[Dict[str, Any]]:
        """Create a tool chain based on a natural language prompt.
        
        Args:
            prompt: Natural language description of the desired workflow
            available_tools: List of available tool names
            
        Returns:
            List of tool specifications for the chain
        """
        # This is a simplified implementation - in a real system, this would use an LLM
        # to analyze the prompt and determine the appropriate tool chain
        
        # For now, we'll create a simple chain based on keywords in the prompt
        chain = []
        
        # Simple keyword-based chain creation
        if "search" in prompt.lower() and "web_search" in available_tools:
            chain.append({
                "name": "web_search",
                "args": {"query": prompt}
            })
        
        if "file" in prompt.lower() and "file_manager" in available_tools:
            chain.append({
                "name": "file_manager",
                "args": {"action": "list", "path": "."}
            })
        
        return chain
    
    def get_chain_history(self) -> List[Dict[str, Any]]:
        """Get the history of executed chains."""
        return self.chain_history.copy()
    
    def validate_chain(self, chain: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate a tool chain before execution.
        
        Args:
            chain: List of tool specifications
            
        Returns:
            Dictionary with validation results
        """
        validation = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        if not isinstance(chain, list):
            validation["valid"] = False
            validation["errors"].append("Chain must be a list")
            return validation
        
        for i, step in enumerate(chain):
            if not isinstance(step, dict):
                validation["valid"] = False
                validation["errors"].append(f"Step {i} must be a dictionary")
                continue
            
            if "name" not in step:
                validation["valid"] = False
                validation["errors"].append(f"Step {i} missing 'name' field")
                continue
            
            tool_name = step["name"]
            if tool_name not in self.tools:
                validation["valid"] = False
                validation["errors"].append(f"Tool '{tool_name}' not found in registry")
        
        return validation