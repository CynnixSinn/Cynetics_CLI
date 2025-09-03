import os
import importlib.util
from typing import Dict, Type
from cynetics.tools.base import BaseTool

def load_plugins(plugin_dir: str = "plugins") -> Dict[str, Type[BaseTool]]:
    """Dynamically load tools from a plugins directory.
    
    Args:
        plugin_dir: Directory containing plugin modules.
        
    Returns:
        A dictionary mapping tool names to their classes.
    """
    plugins = {}
    
    # Check if the plugin directory exists
    if not os.path.exists(plugin_dir):
        return plugins
    
    # Iterate through files in the plugin directory
    for filename in os.listdir(plugin_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]  # Remove .py extension
            module_path = os.path.join(plugin_dir, filename)
            
            # Load the module
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Look for tool classes in the module
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, BaseTool) and 
                    attr != BaseTool):
                    # Register the tool using its name attribute
                    tool_instance = attr()  # Create an instance to access its name
                    tool_name = tool_instance.name
                    plugins[tool_name] = attr
    
    return plugins