from typing import Dict, Any, List
from cynetics.models.provider import ModelProvider

class ContextFusion:
    """A system to merge context from multiple models."""
    
    def __init__(self):
        self.providers = {}
        self.context_history = []
    
    def register_provider(self, name: str, provider: ModelProvider):
        """Register a model provider."""
        self.providers[name] = provider
    
    def generate_with_context(self, prompt: str, providers: List[str], **kwargs) -> Dict[str, Any]:
        """Generate responses from multiple providers and merge context.
        
        Args:
            prompt: The prompt to send to the models.
            providers: List of provider names to use.
            **kwargs: Additional arguments for the model generation.
            
        Returns:
            A dictionary with responses from each provider and a merged context.
        """
        responses = {}
        context_elements = []
        
        # Generate responses from each provider
        for provider_name in providers:
            if provider_name in self.providers:
                try:
                    response = self.providers[provider_name].generate(prompt, **kwargs)
                    responses[provider_name] = response
                    # Extract context elements (simplified for now)
                    context_elements.append({
                        "provider": provider_name,
                        "response": response
                    })
                except Exception as e:
                    responses[provider_name] = {"error": str(e)}
            else:
                responses[provider_name] = {"error": f"Provider '{provider_name}' not found."}
        
        # Merge context (simplified merging logic)
        merged_context = self._merge_context(context_elements)
        
        # Store in history
        self.context_history.append({
            "prompt": prompt,
            "providers": providers,
            "responses": responses,
            "merged_context": merged_context
        })
        
        return {
            "responses": responses,
            "merged_context": merged_context
        }
    
    def _merge_context(self, context_elements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge context elements from multiple sources.
        
        Args:
            context_elements: List of context elements from different providers.
            
        Returns:
            A merged context dictionary.
        """
        # Simplified merging logic - in a real implementation, this would be more sophisticated
        merged = {
            "sources": [],
            "combined_response": "",
            "metadata": {}
        }
        
        for element in context_elements:
            provider = element["provider"]
            response = element["response"]
            
            merged["sources"].append(provider)
            merged["combined_response"] += f"[{provider}]: {response}\n"
            merged["metadata"][provider] = {
                "response_length": len(response),
                "word_count": len(response.split())
            }
        
        return merged
    
    def get_context_history(self) -> List[Dict[str, Any]]:
        """Get the context history."""
        return self.context_history.copy()