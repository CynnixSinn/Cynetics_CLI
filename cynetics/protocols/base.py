from abc import ABC, abstractmethod
from typing import Dict, Any, List

class ProtocolHandler(ABC):
    """Abstract base class for protocol handlers."""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def connect(self, config: Dict[str, Any]) -> bool:
        """Connect to the protocol service.
        
        Args:
            config: Configuration for the connection
            
        Returns:
            True if connected, False otherwise
        """
        pass
    
    @abstractmethod
    def disconnect(self):
        """Disconnect from the protocol service."""
        pass
    
    @abstractmethod
    def execute_action(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action on the protocol.
        
        Args:
            action: Action to execute
            params: Parameters for the action
            
        Returns:
            Result of the action
        """
        pass
    
    @abstractmethod
    def list_actions(self) -> List[str]:
        """List available actions for this protocol.
        
        Returns:
            List of available actions
        """
        pass

class ProtocolManager:
    """Manager for protocol handlers."""
    
    def __init__(self):
        self.handlers: Dict[str, ProtocolHandler] = {}
        self.connections: Dict[str, ProtocolHandler] = {}
    
    def register_handler(self, protocol: str, handler: ProtocolHandler):
        """Register a protocol handler.
        
        Args:
            protocol: Name of the protocol
            handler: Protocol handler instance
        """
        self.handlers[protocol] = handler
    
    def connect(self, protocol: str, config: Dict[str, Any]) -> bool:
        """Connect to a protocol.
        
        Args:
            protocol: Name of the protocol
            config: Configuration for the connection
            
        Returns:
            True if connected, False otherwise
        """
        if protocol not in self.handlers:
            raise ValueError(f"Protocol handler for '{protocol}' not found")
        
        handler = self.handlers[protocol]
        success = handler.connect(config)
        if success:
            self.connections[protocol] = handler
        
        return success
    
    def disconnect(self, protocol: str):
        """Disconnect from a protocol.
        
        Args:
            protocol: Name of the protocol
        """
        if protocol in self.connections:
            self.connections[protocol].disconnect()
            del self.connections[protocol]
    
    def execute_action(self, protocol: str, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an action on a protocol.
        
        Args:
            protocol: Name of the protocol
            action: Action to execute
            params: Parameters for the action
            
        Returns:
            Result of the action
        """
        if protocol not in self.connections:
            raise ValueError(f"Not connected to protocol '{protocol}'")
        
        handler = self.connections[protocol]
        return handler.execute_action(action, params)
    
    def list_protocols(self) -> List[str]:
        """List all registered protocols.
        
        Returns:
            List of registered protocols
        """
        return list(self.handlers.keys())
    
    def list_actions(self, protocol: str) -> List[str]:
        """List available actions for a protocol.
        
        Args:
            protocol: Name of the protocol
            
        Returns:
            List of available actions
        """
        if protocol not in self.handlers:
            raise ValueError(f"Protocol handler for '{protocol}' not found")
        
        return self.handlers[protocol].list_actions()