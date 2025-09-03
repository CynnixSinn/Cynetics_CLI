from typing import Dict, List, Callable, Any
from threading import Lock

class EventSystem:
    """A simple event system for decoupled communication."""
    
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
        self._lock = Lock()
    
    def subscribe(self, event_name: str, callback: Callable):
        """Subscribe to an event."""
        with self._lock:
            if event_name not in self._listeners:
                self._listeners[event_name] = []
            self._listeners[event_name].append(callback)
    
    def unsubscribe(self, event_name: str, callback: Callable) -> bool:
        """Unsubscribe from an event."""
        with self._lock:
            if event_name in self._listeners:
                try:
                    self._listeners[event_name].remove(callback)
                    # Clean up empty listener lists
                    if not self._listeners[event_name]:
                        del self._listeners[event_name]
                    return True
                except ValueError:
                    pass
            return False
    
    def emit(self, event_name: str, data: Any = None):
        """Emit an event to all subscribers."""
        # Get a copy of listeners to avoid modification during iteration
        with self._lock:
            if event_name not in self._listeners:
                return
            listeners_copy = self._listeners[event_name][:]
        
        # Call listeners outside the lock to avoid deadlocks
        for listener in listeners_copy:
            try:
                if data is not None:
                    listener(data)
                else:
                    listener()
            except Exception as e:
                print(f"Error in event listener for {event_name}: {e}")
    
    def get_listeners_count(self, event_name: str) -> int:
        """Get the number of listeners for an event."""
        with self._lock:
            return len(self._listeners.get(event_name, []))
    
    def get_events(self) -> List[str]:
        """Get a list of all events with listeners."""
        with self._lock:
            return list(self._listeners.keys())
    
    def clear_event(self, event_name: str):
        """Remove all listeners for an event."""
        with self._lock:
            if event_name in self._listeners:
                del self._listeners[event_name]
    
    def clear_all(self):
        """Remove all listeners for all events."""
        with self._lock:
            self._listeners.clear()