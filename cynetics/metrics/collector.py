import time
import json
from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict

class MetricsCollector:
    """A simple metrics collector for tracking system performance and usage."""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.counters = defaultdict(int)
        self.gauges = {}
        self.timers = {}
    
    def increment_counter(self, name: str, value: int = 1):
        """Increment a counter metric."""
        self.counters[name] += value
    
    def set_gauge(self, name: str, value: float):
        """Set a gauge metric."""
        self.gauges[name] = value
    
    def start_timer(self, name: str) -> str:
        """Start a timer and return a timer ID."""
        timer_id = f"{name}_{int(time.time() * 1000000)}"
        self.timers[timer_id] = {
            "name": name,
            "start_time": time.time()
        }
        return timer_id
    
    def stop_timer(self, timer_id: str):
        """Stop a timer and record the duration."""
        if timer_id in self.timers:
            timer_info = self.timers.pop(timer_id)
            duration = time.time() - timer_info["start_time"]
            self.metrics[timer_info["name"]].append({
                "value": duration,
                "timestamp": datetime.now().isoformat()
            })
    
    def record_metric(self, name: str, value: float):
        """Record a generic metric value."""
        self.metrics[name].append({
            "value": value,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_counter(self, name: str) -> int:
        """Get the value of a counter."""
        return self.counters.get(name, 0)
    
    def get_gauge(self, name: str) -> float:
        """Get the value of a gauge."""
        return self.gauges.get(name, 0.0)
    
    def get_metrics(self, name: str) -> List[Dict[str, Any]]:
        """Get all recorded values for a metric."""
        return self.metrics.get(name, []).copy()
    
    def get_all_counters(self) -> Dict[str, int]:
        """Get all counters."""
        return dict(self.counters)
    
    def get_all_gauges(self) -> Dict[str, float]:
        """Get all gauges."""
        return dict(self.gauges)
    
    def get_all_metrics(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all metrics."""
        return {k: v.copy() for k, v in self.metrics.items()}
    
    def reset(self):
        """Reset all metrics."""
        self.metrics.clear()
        self.counters.clear()
        self.gauges.clear()
        self.timers.clear()
    
    def summary(self) -> Dict[str, Any]:
        """Get a summary of all metrics."""
        summary = {
            "counters": self.get_all_counters(),
            "gauges": self.get_all_gauges(),
            "metrics": {}
        }
        
        for name, values in self.metrics.items():
            if values:
                # Calculate statistics
                numeric_values = [v["value"] for v in values]
                summary["metrics"][name] = {
                    "count": len(numeric_values),
                    "min": min(numeric_values),
                    "max": max(numeric_values),
                    "avg": sum(numeric_values) / len(numeric_values),
                    "latest": numeric_values[-1] if numeric_values else None
                }
            else:
                summary["metrics"][name] = {
                    "count": 0,
                    "min": None,
                    "max": None,
                    "avg": None,
                    "latest": None
                }
        
        return summary