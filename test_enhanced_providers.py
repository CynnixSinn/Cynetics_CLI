#!/usr/bin/env python3
"""
Test script to verify enhanced model provider support.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_provider_imports():
    """Test that all model providers can be imported."""
    providers = [
        ("OpenAI", "cynetics.models.openai", "OpenAIProvider"),
        ("Ollama", "cynetics.models.ollama", "OllamaProvider"),
        ("Anthropic", "cynetics.models.anthropic", "AnthropicProvider"),
        ("OpenRouter", "cynetics.models.openrouter", "OpenRouterProvider"),
        ("Qwen", "cynetics.models.qwen", "QwenProvider"),
        ("DeepSeek", "cynetics.models.deepseek", "DeepSeekProvider"),
        ("Cohere", "cynetics.models.cohere", "CohereProvider"),
        ("Google", "cynetics.models.google", "GoogleProvider")
    ]
    
    passed = 0
    for name, module, class_name in providers:
        try:
            mod = __import__(module, fromlist=[class_name])
            cls = getattr(mod, class_name)
            print(f"✓ {name} provider loaded: {class_name}")
            passed += 1
        except Exception as e:
            print(f"✗ {name} provider failed: {e}")
    
    print(f"\n{passed}/{len(providers)} providers loaded successfully")
    return passed == len(providers)

def test_provider_registry():
    """Test that providers are registered correctly."""
    try:
        from cynetics.cli.main import MODEL_PROVIDERS
        print(f"✓ Provider registry loaded with {len(MODEL_PROVIDERS)} providers")
        
        expected_providers = {
            "openai", "ollama", "anthropic", "openrouter", 
            "qwen", "deepseek", "cohere", "google"
        }
        
        registered_names = set(MODEL_PROVIDERS.keys())
        missing = expected_providers - registered_names
        extra = registered_names - expected_providers
        
        if missing:
            print(f"⚠ Missing providers in registry: {missing}")
        
        if extra:
            print(f"ℹ Extra providers in registry: {extra}")
            
        if not missing:
            print("✓ All expected providers are registered")
            return True
        else:
            return False
    except Exception as e:
        print(f"✗ Provider registry test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Enhanced Model Provider Support...")
    print("=" * 50)
    print()
    
    tests = [
        test_provider_imports,
        test_provider_registry
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"{passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 All tests passed! Enhanced model provider support is working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
