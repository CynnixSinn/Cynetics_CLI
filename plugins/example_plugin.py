class ExamplePlugin:
    """An example plugin to demonstrate the plugin system."""
    
    __plugin_name__ = "example_plugin"
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.name = "Example Plugin"
        self.version = "1.0.0"
    
    def run(self, input_data: str) -> dict:
        """Run the plugin with input data."""
        return {
            "plugin": self.name,
            "version": self.version,
            "input": input_data,
            "output": f"Processed by {self.name}: {input_data}",
            "status": "success"
        }
    
    def get_info(self) -> dict:
        """Get plugin information."""
        return {
            "name": self.name,
            "version": self.version,
            "description": "An example plugin for the Cynetics CLI plugin system"
        }