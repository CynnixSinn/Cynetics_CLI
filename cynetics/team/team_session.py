import json
import os
from datetime import datetime
from pathlib import Path

class TeamSession:
    """A collaborative session for multiple users."""
    
    def __init__(self, session_id: str, storage_dir: str = "team_sessions"):
        self.session_id = session_id
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.session_file = self.storage_dir / f"{session_id}.json"
        self._load_session()
    
    def _load_session(self):
        """Load session data from file."""
        if self.session_file.exists():
            with open(self.session_file, 'r') as f:
                data = json.load(f)
                self.users = data.get("users", {})
                self.chat_history = data.get("chat_history", [])
                self.shared_context = data.get("shared_context", {})
                self.created_at = data.get("created_at", datetime.now().isoformat())
        else:
            self.users = {}
            self.chat_history = []
            self.shared_context = {}
            self.created_at = datetime.now().isoformat()
            self._save_session()
    
    def _save_session(self):
        """Save session data to file."""
        data = {
            "session_id": self.session_id,
            "created_at": self.created_at,
            "users": self.users,
            "chat_history": self.chat_history,
            "shared_context": self.shared_context
        }
        with open(self.session_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_user(self, user_id: str, user_name: str):
        """Add a user to the session."""
        if user_id not in self.users:
            self.users[user_id] = {
                "name": user_name,
                "joined_at": datetime.now().isoformat(),
                "last_active": datetime.now().isoformat()
            }
            self._save_session()
    
    def send_message(self, user_id: str, message: str):
        """Send a message to the team session."""
        if user_id in self.users:
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
    
    def set_context(self, key: str, value: str):
        """Set a key-value pair in the shared context."""
        self.shared_context[key] = value
        self._save_session()
    
    def get_context(self):
        """Get the shared context."""
        return self.shared_context.copy()
    
    def get_history(self):
        """Get the chat history."""
        return self.chat_history.copy()