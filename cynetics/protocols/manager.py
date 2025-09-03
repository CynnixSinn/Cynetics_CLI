from cynetics.protocols.base import ProtocolManager
from cynetics.protocols.ssh import SSHProtocolHandler
from cynetics.protocols.api import APIProtocolHandler
from cynetics.protocols.git import GitProtocolHandler

def create_protocol_manager() -> ProtocolManager:
    """Create and configure a protocol manager with all available handlers."""
    manager = ProtocolManager()
    
    # Register protocol handlers
    manager.register_handler("ssh", SSHProtocolHandler())
    manager.register_handler("api", APIProtocolHandler())
    manager.register_handler("git", GitProtocolHandler())
    
    return manager