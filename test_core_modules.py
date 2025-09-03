#!/usr/bin/env python3
"""
Test script to verify Cynetics CLI core modules.
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_simple_db():
    """Test the simple database module."""
    print("Testing SimpleDB...")
    try:
        from cynetics.db.simple_db import SimpleDB
        
        # Create a test database
        db = SimpleDB("test_db.json")
        
        # Test setting and getting values
        db.set("test_key", "test_value")
        assert db.get("test_key") == "test_value"
        
        # Test listing keys
        keys = db.list_keys()
        assert "test_key" in keys
        
        # Test deleting values
        assert db.delete("test_key") == True
        assert db.get("test_key") is None
        
        # Test clearing database
        db.set("key1", "value1")
        db.set("key2", "value2")
        db.clear()
        assert len(db.list_keys()) == 0
        
        print("✓ SimpleDB tests passed")
        return True
    except Exception as e:
        print(f"✗ SimpleDB tests failed: {e}")
        return False

def test_task_scheduler():
    """Test the task scheduler module."""
    print("\nTesting TaskScheduler...")
    try:
        from cynetics.scheduler.task_scheduler import TaskScheduler
        import time
        
        scheduler = TaskScheduler()
        scheduler.start()
        
        # Test scheduling a simple task
        result = []
        
        def test_task():
            result.append("executed")
        
        # Schedule task to run immediately
        task_id = scheduler.schedule_task(test_task)
        
        # Wait a moment for task to execute
        time.sleep(0.2)
        
        # Check if task executed
        assert len(result) == 1
        assert result[0] == "executed"
        
        # Stop scheduler
        scheduler.stop()
        
        print("✓ TaskScheduler tests passed")
        return True
    except Exception as e:
        print(f"✗ TaskScheduler tests failed: {e}")
        return False

def test_simple_cache():
    """Test the simple cache module."""
    print("\nTesting SimpleCache...")
    try:
        from cynetics.cache.simple_cache import SimpleCache
        import time
        
        cache = SimpleCache()
        
        # Test setting and getting values
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
        
        # Test TTL functionality
        cache.set("key2", "value2", ttl=1)  # 1 second TTL
        assert cache.get("key2") == "value2"
        
        # Wait for expiration
        time.sleep(1.1)
        assert cache.get("key2") is None
        
        # Test deletion
        cache.set("key3", "value3")
        assert cache.delete("key3") == True
        assert cache.get("key3") is None
        
        # Test existence check
        cache.set("key4", "value4")
        assert cache.has("key4") == True
        assert cache.has("nonexistent") == False
        
        print("✓ SimpleCache tests passed")
        return True
    except Exception as e:
        print(f"✗ SimpleCache tests failed: {e}")
        return False

def test_metrics_collector():
    """Test the metrics collector module."""
    print("\nTesting MetricsCollector...")
    try:
        from cynetics.metrics.collector import MetricsCollector
        
        mc = MetricsCollector()
        
        # Test counter
        mc.increment_counter("test_counter", 5)
        assert mc.get_counter("test_counter") == 5
        
        # Test gauge
        mc.set_gauge("test_gauge", 3.14)
        assert mc.get_gauge("test_gauge") == 3.14
        
        # Test metric recording
        mc.record_metric("test_metric", 42.0)
        metrics = mc.get_metrics("test_metric")
        assert len(metrics) == 1
        assert metrics[0]["value"] == 42.0
        
        # Test summary
        summary = mc.summary()
        assert "counters" in summary
        assert "gauges" in summary
        assert "metrics" in summary
        
        print("✓ MetricsCollector tests passed")
        return True
    except Exception as e:
        print(f"✗ MetricsCollector tests failed: {e}")
        return False

def test_config_manager():
    """Test the configuration manager module."""
    print("\nTesting ConfigManager...")
    try:
        from cynetics.config.manager import ConfigManager
        import tempfile
        import json
        
        # Create a temporary config file
        config_data = {
            "database": {
                "host": "localhost",
                "port": 5432
            },
            "api": {
                "key": "secret123"
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        # Test loading config
        cm = ConfigManager(config_file)
        
        # Test getting values
        assert cm.get("database.host") == "localhost"
        assert cm.get("database.port") == 5432
        assert cm.get("api.key") == "secret123"
        
        # Test setting values
        cm.set("new_setting", "new_value")
        assert cm.get("new_setting") == "new_value"
        
        # Test checking existence
        assert cm.has("database") == True
        assert cm.has("nonexistent") == False
        
        # Clean up
        os.unlink(config_file)
        
        print("✓ ConfigManager tests passed")
        return True
    except Exception as e:
        print(f"✗ ConfigManager tests failed: {e}")
        return False

def test_event_system():
    """Test the event system module."""
    print("\nTesting EventSystem...")
    try:
        from cynetics.events.system import EventSystem
        
        es = EventSystem()
        
        # Test event subscription and emission
        events_received = []
        
        def test_listener(data=None):
            events_received.append(data or "received")
        
        # Subscribe to an event
        es.subscribe("test_event", test_listener)
        
        # Emit the event
        es.emit("test_event", "test_data")
        
        # Check if event was received
        assert len(events_received) == 1
        assert events_received[0] == "test_data"
        
        # Test unsubscribing
        assert es.unsubscribe("test_event", test_listener) == True
        es.emit("test_event", "test_data2")
        assert len(events_received) == 1  # Should not have received the second event
        
        print("✓ EventSystem tests passed")
        return True
    except Exception as e:
        print(f"✗ EventSystem tests failed: {e}")
        return False

def test_plugin_manager():
    """Test the plugin manager module."""
    print("\nTesting PluginManager...")
    try:
        from cynetics.plugins.manager import PluginManager
        
        pm = PluginManager(["plugins"])
        
        # Load plugins
        loaded_count = pm.load_all_plugins()
        
        # Check if example plugin was loaded
        plugin = pm.get_plugin("example_plugin")
        assert plugin is not None
        
        # Check if example plugin class was registered
        plugin_class = pm.get_plugin_class("example_plugin")
        assert plugin_class is not None
        
        # Test instantiating plugin
        instance = pm.instantiate_plugin("example_plugin")
        assert instance is not None
        
        # Test plugin functionality
        info = instance.get_info()
        assert info["name"] == "Example Plugin"
        
        result = instance.run("test input")
        assert result["status"] == "success"
        assert "test input" in result["output"]
        
        print("✓ PluginManager tests passed")
        return True
    except Exception as e:
        print(f"✗ PluginManager tests failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Cynetics CLI Core Modules Test Suite")
    print("=" * 40)
    
    tests = [
        test_simple_db,
        test_task_scheduler,
        test_simple_cache,
        test_metrics_collector,
        test_config_manager,
        test_event_system,
        test_plugin_manager
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"Passed: {passed}/{total} tests")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())