import json
import os
from typing import Dict, Any, List
from datetime import datetime

class SimpleDB:
    """A simple file-based database for storing team session data."""
    
    def __init__(self, db_path: str = "cynetics_db.json"):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Ensure the database file exists."""
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                json.dump({}, f)
    
    def _load_db(self) -> Dict[str, Any]:
        """Load the database from file."""
        with open(self.db_path, 'r') as f:
            return json.load(f)
    
    def _save_db(self, data: Dict[str, Any]):
        """Save the database to file."""
        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def get(self, key: str) -> Any:
        """Get a value by key."""
        db = self._load_db()
        return db.get(key)
    
    def set(self, key: str, value: Any):
        """Set a value by key."""
        db = self._load_db()
        db[key] = value
        self._save_db(db)
    
    def delete(self, key: str) -> bool:
        """Delete a key from the database."""
        db = self._load_db()
        if key in db:
            del db[key]
            self._save_db(db)
            return True
        return False
    
    def list_keys(self) -> List[str]:
        """List all keys in the database."""
        db = self._load_db()
        return list(db.keys())
    
    def clear(self):
        """Clear all data from the database."""
        self._save_db({})