#!/usr/bin/env python3
"""
Test script for the simplified Cynetics CLI.
"""

import os
import sys
import tempfile
import subprocess

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that we can import the simplified CLI."""
    try:
        from cynetics_simple import load_or_create_config
        print("✓ Successfully imported simplified CLI")
        return True
    except Exception as e:
        print(f"✗ Failed to import simplified CLI: {e}")
        return False

def test_config_creation():
    """Test creating a basic config."""
    try:
        import yaml
        
        # Create a test config
        test_config = {
            "model_providers": {
                "ollama": {
                    "host": "http://localhost:11434",
                    "model": "llama3"
                }
            },
            "tools": {
                "enabled": ["file_manager"]
            },
            "tui_enabled": True
        }
        
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.yaml') as f:
            temp_config = f.name
            yaml.dump(test_config, f)
        
        # Verify we can read it back
        with open(temp_config, 'r') as f:
            loaded_config = yaml.safe_load(f)
        
        # Clean up
        os.unlink(temp_config)
        
        print("✓ Successfully created and read test configuration")
        return True
    except Exception as e:
        print(f"✗ Failed to create test configuration: {e}")
        return False

if __name__ == "__main__":
    print("Testing simplified Cynetics CLI...")
    
    success = True
    success &= test_imports()
    success &= test_config_creation()
    
    if success:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)