from typing import Dict, Any, List
from cynetics.protocols.base import ProtocolHandler
import requests
import json

class APIProtocolHandler(ProtocolHandler):
    """Generic API protocol handler."""
    
    def __init__(self):
        super().__init__("api")
        self.connected = False
        self.base_url = None
        self.headers = {}
        self.session = None
    
    def connect(self, config: Dict[str, Any]) -> bool:
        """Connect to API service."""
        self.base_url = config.get("base_url")
        self.headers = config.get("headers", {})
        
        if not self.base_url:
            return False
        
        # Create a session for making requests
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        self.connected = True
        return True
    
    def disconnect(self):
        """Disconnect from API service."""
        if self.session:
            self.session.close()
        
        self.connected = False
        self.base_url = None
        self.headers = {}
        self.session = None
    
    def execute_action(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an API action."""
        if not self.connected:
            return {"error": "Not connected to API service"}
        
        if not self.session:
            return {"error": "No active session"}
        
        method = params.get("method", "GET").upper()
        endpoint = params.get("endpoint", "")
        data = params.get("data", {})
        headers = params.get("headers", {})
        
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data if method in ["POST", "PUT", "PATCH"] else None,
                params=data if method in ["GET", "DELETE"] else None,
                headers=headers
            )
            
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.text,
                "json": response.json() if response.headers.get("content-type", "").startswith("application/json") else None
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"error": str(e)}
    
    def list_actions(self) -> List[str]:
        """List available API actions."""
        return ["request"]  # Generic request action