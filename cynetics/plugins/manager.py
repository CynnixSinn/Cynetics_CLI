import os
import importlib.util
from typing import Dict, Any, List, Type
from pathlib import Path

class PluginManager:
    """A simple plugin manager for loading and managing plugins."""
    
    def __init__(self, plugin_dirs: List[str] = None):
        self.plugin_dirs = plugin_dirs or ["plugins"]
        self.plugins: Dict[str, Any] = {}
        self.plugin_classes: Dict[str, Type] = {}
    
    def discover_plugins(self) -> List[str]:
        """Discover all plugin files."""
        plugin_files = []
        
        for plugin_dir in self.plugin_dirs:
            if os.path.exists(plugin_dir):
                for file in os.listdir(plugin_dir):
                    if file.endswith(".py") and not file.startswith("__"):
                        plugin_files.append(os.path.join(plugin_dir, file))
        
        return plugin_files
    
    def load_plugin(self, plugin_path: str) -> bool:
        """Load a plugin from a file."""
        try:
            # Get module name from file path
            module_name = Path(plugin_path).stem
            
            # Load the module
            spec = importlib.util.spec_from_file_location(module_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Store the module
            self.plugins[module_name] = module
            
            # Look for plugin classes
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and hasattr(attr, '__plugin_name__'):
                    plugin_name = getattr(attr, '__plugin_name__', attr_name)
                    self.plugin_classes[plugin_name] = attr
            
            return True
        except Exception as e:
            print(f"Failed to load plugin {plugin_path}: {e}")
            return False
    
    def load_all_plugins(self):
        """Load all discovered plugins."""
        plugin_files = self.discover_plugins()
        loaded_count = 0
        
        for plugin_file in plugin_files:
            if self.load_plugin(plugin_file):
                loaded_count += 1
        
        return loaded_count
    
    def get_plugin(self, name: str) -> Any:
        """Get a loaded plugin by name."""
        return self.plugins.get(name)
    
    def get_plugin_class(self, name: str) -> Type:
        """Get a plugin class by name."""
        return self.plugin_classes.get(name)
    
    def get_all_plugins(self) -> Dict[str, Any]:
        """Get all loaded plugins."""
        return self.plugins.copy()
    
    def get_all_plugin_classes(self) -> Dict[str, Type]:
        """Get all plugin classes."""
        return self.plugin_classes.copy()
    
    def unload_plugin(self, name: str) -> bool:
        """Unload a plugin."""
        if name in self.plugins:
            del self.plugins[name]
            # Also remove any associated classes
            classes_to_remove = [cls_name for cls_name, cls in self.plugin_classes.items() 
                               if cls.__module__ == name]
            for cls_name in classes_to_remove:
                del self.plugin_classes[cls_name]
            return True
        return False
    
    def reload_plugin(self, name: str) -> bool:
        """Reload a plugin."""
        if name in self.plugins:
            plugin_path = self.plugins[name].__file__
            self.unload_plugin(name)
            return self.load_plugin(plugin_path)
        return False
    
    def instantiate_plugin(self, class_name: str, *args, **kwargs) -> Any:
        """Instantiate a plugin class."""
        plugin_class = self.plugin_classes.get(class_name)
        if plugin_class:
            return plugin_class(*args, **kwargs)
        return None