from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTool(ABC):
    """Abstract base class for MCP tools."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool with given arguments."""
        pass