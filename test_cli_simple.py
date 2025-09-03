#!/usr/bin/env python3
"""
Simple test script to verify Cynetics CLI functionality.
"""

import subprocess
import sys
import os

def test_cli_help():
    """Test that the CLI help command works."""
    try:
        result = subprocess.run([
            sys.executable, "-m", "cynetics.cli.main", "--help"
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0 and "Usage:" in result.stdout:
            print("✓ CLI help command works")
            return True
        else:
            print(f"✗ CLI help command failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ CLI help test failed: {e}")
        return False

def test_cli_version():
    """Test that the CLI version command works."""
    try:
        result = subprocess.run([
            sys.executable, "-m", "cynetics.cli.main", "run", "--version"
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0 and "Cynetics CLI v" in result.stdout:
            print("✓ CLI version command works")
            return True
        else:
            print(f"✗ CLI version command failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ CLI version test failed: {e}")
        return False

def test_cli_personality():
    """Test that the CLI personality command works."""
    try:
        result = subprocess.run([
            sys.executable, "-m", "cynetics.cli.main", "personality", "--list-modes"
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0 and "Available personality modes:" in result.stdout:
            print("✓ CLI personality command works")
            return True
        else:
            print(f"✗ CLI personality command failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ CLI personality test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Running Cynetics CLI tests...\n")
    
    tests = [
        test_cli_help,
        test_cli_version,
        test_cli_personality
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n{passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())