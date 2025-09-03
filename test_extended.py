#!/usr/bin/env python3
"""
Extended test script to verify Cynetics CLI functionality with new tools.
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from cynetics.config import load_config
from cynetics.tools import load_tool
from cynetics.tools.chain import ToolChain

def test_config_loading():
    """Test loading configuration."""
    print("Testing configuration loading...")
    try:
        config = load_config("config.yaml")
        print(f"✓ Configuration loaded successfully")
        print(f"  Model providers: {list(config.model_providers.keys())}")
        print(f"  Enabled tools: {config.tools.get('enabled', [])}")
        return True
    except Exception as e:
        print(f"✗ Configuration loading failed: {e}")
        return False

def test_tool_loading():
    """Test loading tools."""
    print("\nTesting tool loading...")
    try:
        config = load_config("config.yaml")
        enabled_tools = config.tools.get("enabled", [])
        
        for tool_name in enabled_tools:
            try:
                tool = load_tool(tool_name)
                print(f"✓ Tool '{tool_name}' loaded successfully")
                print(f"  Description: {tool.description}")
            except Exception as e:
                print(f"✗ Tool '{tool_name}' failed to load: {e}")
                return False
        return True
    except Exception as e:
        print(f"✗ Tool loading test failed: {e}")
        return False

def test_advanced_tools():
    """Test advanced tools."""
    print("\nTesting advanced tools...")
    
    # Test web search tool
    try:
        search_tool = load_tool("advanced_web_search")
        result = search_tool.run("Python programming", ["duckduckgo"], 3)
        if result["status"] == "success":
            print("✓ Advanced web search tool works")
            print(f"  Found {result['total_results']} results")
        else:
            print(f"✗ Advanced web search failed: {result.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"✗ Advanced web search test failed: {e}")
        return False
    
    # Test system monitor tool
    try:
        monitor_tool = load_tool("system_monitor")
        result = monitor_tool.run("cpu", 1)
        if result["status"] == "success":
            print("✓ System monitor tool works")
            print(f"  CPU usage: {result['total_cpu_usage']:.2f}%")
        else:
            print(f"✗ System monitor failed: {result.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"✗ System monitor test failed: {e}")
        return False
    
    return True

def test_tool_chaining():
    """Test tool chaining functionality."""
    print("\nTesting tool chaining...")
    
    try:
        # Create a tool chain
        chain = ToolChain()
        
        # Register tools
        for tool_name in ["file_manager", "web_search"]:
            tool = load_tool(tool_name)
            chain.register_tool(tool_name, tool)
        
        # Create a simple chain
        chain_spec = [
            {
                "name": "file_manager",
                "args": {"action": "list", "path": "."}
            },
            {
                "name": "web_search",
                "args": {"query": "Python file management"}
            }
        ]
        
        # Execute the chain
        result = chain.execute_chain(chain_spec)
        
        if result["success"]:
            print("✓ Tool chaining works")
            print(f"  Chain executed {len(result['chain_results'])} steps")
        else:
            print(f"✗ Tool chaining failed: {result.get('errors', 'Unknown error')}")
            return False
            
        return True
    except Exception as e:
        print(f"✗ Tool chaining test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Cynetics CLI Extended Test Suite")
    print("=" * 40)
    
    success = True
    success &= test_config_loading()
    success &= test_tool_loading()
    success &= test_advanced_tools()
    success &= test_tool_chaining()
    
    print("\n" + "=" * 40)
    if success:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
