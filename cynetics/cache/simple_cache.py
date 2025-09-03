import time
from typing import Any, Dict, Optional
from threading import Lock

class SimpleCache:
    """A simple in-memory cache with TTL support."""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in the cache with an optional TTL (time to live) in seconds."""
        with self._lock:
            expiry = None
            if ttl is not None:
                expiry = time.time() + ttl
                
            self._cache[key] = {
                "value": value,
                "expiry": expiry
            }
    
    def get(self, key: str) -> Any:
        """Get a value from the cache, returning None if not found or expired."""
        with self._lock:
            if key not in self._cache:
                return None
                
            entry = self._cache[key]
            
            # Check if entry has expired
            if entry["expiry"] is not None and time.time() > entry["expiry"]:
                del self._cache[key]
                return None
                
            return entry["value"]
    
    def delete(self, key: str) -> bool:
        """Delete a key from the cache."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """Clear all entries from the cache."""
        with self._lock:
            self._cache.clear()
    
    def has(self, key: str) -> bool:
        """Check if a key exists in the cache and hasn't expired."""
        with self._lock:
            if key not in self._cache:
                return False
                
            entry = self._cache[key]
            
            # Check if entry has expired
            if entry["expiry"] is not None and time.time() > entry["expiry"]:
                del self._cache[key]
                return False
                
            return True
    
    def size(self) -> int:
        """Get the number of entries in the cache."""
        with self._lock:
            # Clean up expired entries
            expired_keys = []
            current_time = time.time()
            
            for key, entry in self._cache.items():
                if entry["expiry"] is not None and current_time > entry["expiry"]:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._cache[key]
                
            return len(self._cache)
    
    def keys(self) -> list:
        """Get all keys in the cache."""
        with self._lock:
            # Clean up expired entries
            expired_keys = []
            current_time = time.time()
            
            for key, entry in self._cache.items():
                if entry["expiry"] is not None and current_time > entry["expiry"]:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._cache[key]
                
            return list(self._cache.keys())