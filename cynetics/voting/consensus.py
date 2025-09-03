from typing import Dict, Any, List, Callable
from collections import Counter
import random

class ModelVoting:
    """A system for model voting and consensus."""
    
    def __init__(self):
        self.providers = {}
    
    def register_provider(self, name: str, provider):
        """Register a model provider."""
        self.providers[name] = provider
    
    def majority_vote(self, prompt: str, providers: List[str], **kwargs) -> Dict[str, Any]:
        """Get responses from multiple providers and determine the majority vote.
        
        Args:
            prompt: The prompt to send to the models.
            providers: List of provider names to use.
            **kwargs: Additional arguments for the model generation.
            
        Returns:
            A dictionary with individual responses and the majority vote.
        """
        responses = {}
        response_counts = Counter()
        
        # Get responses from each provider
        for provider_name in providers:
            if provider_name in self.providers:
                try:
                    response = self.providers[provider_name].generate(prompt, **kwargs)
                    responses[provider_name] = response
                    response_counts[response] += 1
                except Exception as e:
                    responses[provider_name] = {"error": str(e)}
            else:
                responses[provider_name] = {"error": f"Provider '{provider_name}' not found."}
        
        # Determine the majority vote
        if response_counts:
            majority_response = response_counts.most_common(1)[0][0]
            majority_count = response_counts.most_common(1)[0][1]
        else:
            majority_response = None
            majority_count = 0
        
        return {
            "responses": responses,
            "majority_vote": majority_response,
            "majority_count": majority_count,
            "total_responses": len(providers)
        }
    
    def weighted_voting(self, prompt: str, providers: List[str], weights: Dict[str, float], **kwargs) -> Dict[str, Any]:
        """Get responses from multiple providers and determine the weighted vote.
        
        Args:
            prompt: The prompt to send to the models.
            providers: List of provider names to use.
            weights: Dictionary mapping provider names to weights.
            **kwargs: Additional arguments for the model generation.
            
        Returns:
            A dictionary with individual responses and the weighted vote.
        """
        responses = {}
        weighted_scores = {}
        
        # Get responses from each provider
        for provider_name in providers:
            if provider_name in self.providers:
                try:
                    response = self.providers[provider_name].generate(prompt, **kwargs)
                    responses[provider_name] = response
                    
                    # Calculate weighted score (simplified)
                    weight = weights.get(provider_name, 1.0)
                    # In a real implementation, you might use a more sophisticated scoring method
                    # For now, we'll just use the weight as the score
                    weighted_scores[response] = weighted_scores.get(response, 0) + weight
                except Exception as e:
                    responses[provider_name] = {"error": str(e)}
            else:
                responses[provider_name] = {"error": f"Provider '{provider_name}' not found."}
        
        # Determine the weighted vote
        if weighted_scores:
            weighted_vote = max(weighted_scores, key=weighted_scores.get)
            max_score = weighted_scores[weighted_vote]
        else:
            weighted_vote = None
            max_score = 0
        
        return {
            "responses": responses,
            "weighted_vote": weighted_vote,
            "max_score": max_score,
            "weighted_scores": weighted_scores
        }
    
    def best_of_n(self, prompt: str, provider: str, n: int, scoring_fn: Callable[[str], float], **kwargs) -> Dict[str, Any]:
        """Generate N responses from a single provider and select the best one.
        
        Args:
            prompt: The prompt to send to the model.
            provider: Provider name to use.
            n: Number of responses to generate.
            scoring_fn: Function to score responses (higher is better).
            **kwargs: Additional arguments for the model generation.
            
        Returns:
            A dictionary with all responses and the best one.
        """
        if provider not in self.providers:
            return {"error": f"Provider '{provider}' not found."}
        
        responses = []
        scores = []
        
        # Generate N responses
        for i in range(n):
            try:
                response = self.providers[provider].generate(prompt, **kwargs)
                responses.append(response)
                scores.append(scoring_fn(response))
            except Exception as e:
                responses.append({"error": str(e)})
                scores.append(-float('inf'))  # Assign lowest score to errors
        
        # Find the best response
        if responses:
            best_index = scores.index(max(scores))
            best_response = responses[best_index]
            best_score = scores[best_index]
        else:
            best_response = None
            best_score = -float('inf')
        
        return {
            "responses": responses,
            "scores": scores,
            "best_response": best_response,
            "best_score": best_score
        }

# Simple consensus function
def consensus(responses: List[str]) -> str:
    """Simple consensus function that returns the most common response."""
    if not responses:
        return ""
    
    counter = Counter(responses)
    return counter.most_common(1)[0][0]