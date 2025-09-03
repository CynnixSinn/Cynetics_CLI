import threading
import time
import json
import os
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path

class TeamSession:
    """A collaborative session for multiple users."""
    
    def __init__(self, session_id: str, storage_dir: str = "team_sessions"):
        self.session_id = session_id
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.session_file = self.storage_dir / f"{session_id}.json"
        self.lock = threading.Lock()
        self._load_session()
    
    def _load_session(self):
        """Load session data from file."""
        if self.session_file.exists():
            with open(self.session_file, 'r') as f:
                data = json.load(f)
                self.users = data.get("users", {})
                self.chat_history = data.get("chat_history", [])
                self.shared_context = data.get("shared_context", {})
                self.created_at = datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
        else:
            self.users = {}
            self.chat_history = []
            self.shared_context = {}
            self.created_at = datetime.now()
            self._save_session()
    
    def _save_session(self):
        """Save session data to file."""
        data = {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "users": self.users,
            "chat_history": self.chat_history,
            "shared_context": self.shared_context
        }
        with open(self.session_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_user(self, user_id: str, user_name: str) -> bool:
        """Add a user to the session."""
        with self.lock:
            self._load_session()
            if user_id in self.users:
                return False
            
            self.users[user_id] = {
                "name": user_name,
                "joined_at": datetime.now().isoformat(),
                "last_active": datetime.now().isoformat()
            }
            self._save_session()
            return True
    
    def remove_user(self, user_id: str) -> bool:
        """Remove a user from the session."""
        with self.lock:
            self._load_session()
            if user_id in self.users:
                del self.users[user_id]
                self._save_session()
                return True
            return False
    
    def send_message(self, user_id: str, message: str) -> bool:
        """Send a message to the team session."""
        with self.lock:
            self._load_session()
            if user_id not in self.users:
                return False
            
            # Update user's last active time
            self.users[user_id]["last_active"] = datetime.now().isoformat()
            
            # Add message to chat history
            self.chat_history.append({
                "user_id": user_id,
                "user_name": self.users[user_id]["name"],
                "message": message,
                "timestamp": datetime.now().isoformat()
            })
            self._save_session()
            return True
    
    def update_context(self, user_id: str, key: str, value: Any) -> bool:
        """Update the shared context."""
        with self.lock:
            self._load_session()
            if user_id not in self.users:
                return False
            
            # Update user's last active time
            self.users[user_id]["last_active"] = datetime.now().isoformat()
            
            # Update shared context
            self.shared_context[key] = value
            self._save_session()
            return True
    
    def get_chat_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent chat history."""
        with self.lock:
            self._load_session()
            # Return the most recent messages
            return self.chat_history[-limit:] if len(self.chat_history) > limit else self.chat_history
    
    def get_shared_context(self) -> Dict[str, Any]:
        """Get the shared context."""
        with self.lock:
            self._load_session()
            # Return a copy of the shared context
            return self.shared_context.copy()
    
    def get_users(self) -> Dict[str, Dict[str, Any]]:
        """Get the list of users in the session."""
        with self.lock:
            self._load_session()
            # Return a copy of the users dictionary
            return {user_id: user_info.copy() for user_id, user_info in self.users.items()}
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get information about the session."""
        with self.lock:
            self._load_session()
            return {
                "session_id": self.session_id,
                "created_at": self.created_at.isoformat(),
                "user_count": len(self.users),
                "message_count": len(self.chat_history),
                "users": self.get_users()
            }

class TeamModeManager:
    """Manager for team mode sessions."""
    
    def __init__(self, storage_dir: str = "team_sessions"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.lock = threading.Lock()
    
    def create_session(self, session_id: str) -> TeamSession:
        """Create a new team session."""
        with self.lock:
            session_file = self.storage_dir / f"{session_id}.json"
            if session_file.exists():
                raise ValueError(f"Session '{session_id}' already exists")
            
            session = TeamSession(session_id, self.storage_dir)
            return session
    
    def get_session(self, session_id: str) -> TeamSession:
        """Get a team session by ID."""
        session_file = self.storage_dir / f"{session_id}.json"
        if not session_file.exists():
            return None
        return TeamSession(session_id, self.storage_dir)
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a team session."""
        with self.lock:
            session_file = self.storage_dir / f"{session_id}.json"
            if session_file.exists():
                session_file.unlink()
                return True
            return False
    
    def list_sessions(self) -> List[str]:
        """List all active sessions."""
        with self.lock:
            session_files = self.storage_dir.glob("*.json")
            return [f.stem for f in session_files]

# Global team mode manager
team_manager = TeamModeManager()