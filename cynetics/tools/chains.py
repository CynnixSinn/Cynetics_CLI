from typing import List, Dict, Any, Callable
from cynetics.tools.base import BaseTool
import asyncio
import json

class ToolChain:
    """A system for chaining multiple tools together."""
    
    def __init__(self, tools: Dict[str, BaseTool]):
        self.tools = tools
        self.chain_history = []
    
    def add_tool(self, name: str, tool: BaseTool):
        """Add a tool to the chain system."""
        self.tools[name] = tool
    
    def execute_chain(self, chain: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute a chain of tools.
        
        Args:
            chain: List of tool calls with their parameters
            
        Returns:
            Dictionary with results from each tool in the chain
        """
        results = {
            "chain_results": [],
            "final_output": None,
            "success": True,
            "error": None
        }
        
        context = {}  # Shared context between tools
        
        try:
            for i, step in enumerate(chain):
                tool_name = step.get("tool")
                params = step.get("params", {})
                
                if tool_name not in self.tools:
                    raise ValueError(f"Tool '{tool_name}' not found")
                
                # Merge context with parameters
                merged_params = {**context, **params}
                
                # Execute the tool
                tool_result = self.tools[tool_name].run(**merged_params)
                
                # Store result
                step_result = {
                    "step": i + 1,
                    "tool": tool_name,
                    "params": params,
                    "result": tool_result
                }
                results["chain_results"].append(step_result)
                
                # Update context with results that have data
                if isinstance(tool_result, dict) and tool_result.get("status") == "success":
                    # Add all result data to context for next tools
                    context.update({f"{tool_name}_{k}": v for k, v in tool_result.items() if k != "status"})
                
                # Check for early termination
                if isinstance(tool_result, dict) and tool_result.get("terminate_chain", False):
                    break
            
            # Set final output as the result of the last tool
            if results["chain_results"]:
                results["final_output"] = results["chain_results"][-1]["result"]
                
        except Exception as e:
            results["success"] = False
            results["error"] = str(e)
        
        # Store in history
        self.chain_history.append({
            "chain": chain,
            "results": results,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        })
        
        return results
    
    async def execute_chain_async(self, chain: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute a chain of tools asynchronously.
        
        Args:
            chain: List of tool calls with their parameters
            
        Returns:
            Dictionary with results from each tool in the chain
        """
        results = {
            "chain_results": [],
            "final_output": None,
            "success": True,
            "error": None
        }
        
        context = {}  # Shared context between tools
        
        try:
            for i, step in enumerate(chain):
                tool_name = step.get("tool")
                params = step.get("params", {})
                
                if tool_name not in self.tools:
                    raise ValueError(f"Tool '{tool_name}' not found")
                
                # Merge context with parameters
                merged_params = {**context, **params}
                
                # Execute the tool asynchronously if it supports it
                tool = self.tools[tool_name]
                if hasattr(tool, 'run_async'):
                    tool_result = await tool.run_async(**merged_params)
                else:
                    # Fallback to synchronous execution
                    tool_result = tool.run(**merged_params)
                
                # Store result
                step_result = {
                    "step": i + 1,
                    "tool": tool_name,
                    "params": params,
                    "result": tool_result
                }
                results["chain_results"].append(step_result)
                
                # Update context with results that have data
                if isinstance(tool_result, dict) and tool_result.get("status") == "success":
                    # Add all result data to context for next tools
                    context.update({f"{tool_name}_{k}": v for k, v in tool_result.items() if k != "status"})
                
                # Check for early termination
                if isinstance(tool_result, dict) and tool_result.get("terminate_chain", False):
                    break
            
            # Set final output as the result of the last tool
            if results["chain_results"]:
                results["final_output"] = results["chain_results"][-1]["result"]
                
        except Exception as e:
            results["success"] = False
            results["error"] = str(e)
        
        # Store in history
        self.chain_history.append({
            "chain": chain,
            "results": results,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        })
        
        return results
    
    def get_chain_history(self) -> List[Dict[str, Any]]:
        """Get the chain execution history."""
        return self.chain_history.copy()
    
    def create_chain_from_description(self, description: str, available_tools: List[str]) -> List[Dict[str, Any]]:
        """Create a tool chain based on a natural language description.
        
        Args:
            description: Natural language description of the desired workflow
            available_tools: List of available tool names
            
        Returns:
            List representing the tool chain
        """
        # This is a simplified implementation
        # In a real system, this would use an LLM to plan the chain
        chain = []
        
        # Simple keyword-based chain creation (for demonstration)
        if "search" in description.lower() and "web_search" in available_tools:
            chain.append({
                "tool": "web_search",
                "params": {"query": description}
            })
        
        if "file" in description.lower() and "file_manager" in available_tools:
            chain.append({
                "tool": "file_manager",
                "params": {"action": "list"}
            })
        
        return chain
    
    def validate_chain(self, chain: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate a tool chain for execution.
        
        Args:
            chain: List of tool calls to validate
            
        Returns:
            Dictionary with validation results
        """
        validation = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        for i, step in enumerate(chain):
            tool_name = step.get("tool")
            params = step.get("params", {})
            
            if not tool_name:
                validation["valid"] = False
                validation["errors"].append(f"Step {i+1}: Missing tool name")
                continue
                
            if tool_name not in self.tools:
                validation["valid"] = False
                validation["errors"].append(f"Step {i+1}: Tool '{tool_name}' not found")
                continue
                
            # Check for required parameters (simplified)
            # In a real implementation, this would check against the tool's schema
            if not isinstance(params, dict):
                validation["warnings"].append(f"Step {i+1}: Parameters should be a dictionary")
        
        return validation