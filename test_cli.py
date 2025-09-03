#!/usr/bin/env python3
"""
Test script to verify Cynetics CLI core functionality.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_config_loading():
    """Test that config loading works."""
    try:
        from cynetics.config_module import load_config
        config = load_config("config.yaml")
        print("✓ Config loading works")
        return True
    except Exception as e:
        print(f"✗ Config loading failed: {e}")
        return False

def test_model_provider():
    """Test that model provider loading works."""
    try:
        from cynetics.models.provider import ModelProvider
        print("✓ Model provider loading works")
        return True
    except Exception as e:
        print(f"✗ Model provider loading failed: {e}")
        return False

def test_cli_commands():
    """Test that CLI commands are available."""
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "cynetics.cli", "--help"
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0 and "Commands:" in result.stdout:
            print("✓ CLI commands are available")
            return True
        else:
            print(f"✗ CLI commands failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ CLI commands test failed: {e}")
        return False

def test_tools_registry():
    """Test that tools registry works."""
    try:
        from cynetics.tools import load_tool, TOOL_REGISTRY
        print(f"✓ Tools registry works ({len(TOOL_REGISTRY)} tools available)")
        return True
    except Exception as e:
        print(f"✗ Tools registry failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Running Cynetics CLI tests...\\n")
    
    tests = [
        test_config_loading,
        test_model_provider,
        test_cli_commands,
        test_tools_registry
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\\n{passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())