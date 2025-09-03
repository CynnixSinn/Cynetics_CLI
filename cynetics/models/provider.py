from abc import ABC, abstractmethod
from typing import Any

class ModelProvider(ABC):
    """Abstract base class for model providers."""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the model."""
        pass

    @abstractmethod
    def configure(self, config: dict):
        """Configure the model provider with settings."""
        pass