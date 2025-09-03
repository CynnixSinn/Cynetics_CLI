import requests
from typing import Dict, Any, List
from cynetics.tools.base import BaseTool

class AdvancedWebSearchTool(BaseTool):
    """An advanced web search tool that uses multiple search engines."""
    
    def __init__(self):
        super().__init__(
            name="advanced_web_search",
            description="Perform advanced web searches using multiple search engines with result aggregation."
        )
        self.search_engines = {
            "duckduckgo": self._search_duckduckgo,
            "google": self._search_google,
            "bing": self._search_bing
        }
    
    def run(self, query: str, engines: List[str] = None, max_results: int = 5) -> Dict[str, Any]:
        """Perform an advanced web search.
        
        Args:
            query: The search query.
            engines: List of search engines to use (default: all).
            max_results: Maximum number of results to return per engine.
            
        Returns:
            A dictionary with the search results.
        """
        if engines is None:
            engines = list(self.search_engines.keys())
        
        results = {
            "status": "success",
            "query": query,
            "engines_used": [],
            "all_results": {},
            "aggregated_results": [],
            "total_results": 0
        }
        
        # Search each engine
        for engine in engines:
            if engine in self.search_engines:
                try:
                    engine_results = self.search_engines[engine](query, max_results)
                    results["engines_used"].append(engine)
                    results["all_results"][engine] = engine_results
                    results["total_results"] += len(engine_results)
                except Exception as e:
                    results[f"{engine}_error"] = str(e)
        
        # Aggregate results, removing duplicates
        seen_urls = set()
        for engine, engine_results in results["all_results"].items():
            for result in engine_results:
                url = result.get("url", "")
                if url not in seen_urls:
                    seen_urls.add(url)
                    results["aggregated_results"].append(result)
        
        # Limit to max_results
        results["aggregated_results"] = results["aggregated_results"][:max_results]
        
        return results
    
    def _search_duckduckgo(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search using DuckDuckGo Instant Answer API."""
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": "1",
            "skip_disambig": "1"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        results = []
        
        # Add abstract as first result if available
        if data.get("AbstractText"):
            results.append({
                "title": data.get("Heading", query),
                "url": data.get("AbstractURL", ""),
                "snippet": data.get("AbstractText", ""),
                "source": "duckduckgo"
            })
        
        # Add related topics
        related_topics = data.get("RelatedTopics", [])
        for topic in related_topics[:max_results]:
            if "FirstURL" in topic and "Text" in topic:
                results.append({
                    "title": topic["Text"],
                    "url": topic["FirstURL"],
                    "snippet": "",
                    "source": "duckduckgo"
                })
        
        return results
    
    def _search_google(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search using Google Custom Search API (stub implementation)."""
        # This is a stub - in a real implementation, you would need a Google API key
        # and use the Google Custom Search API
        return [{
            "title": f"Google search results for: {query}",
            "url": "https://www.google.com",
            "snippet": "This is a stub implementation. In a real system, this would connect to Google's API.",
            "source": "google"
        }]
    
    def _search_bing(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search using Bing Search API (stub implementation)."""
        # This is a stub - in a real implementation, you would need a Bing API key
        # and use the Bing Search API
        return [{
            "title": f"Bing search results for: {query}",
            "url": "https://www.bing.com",
            "snippet": "This is a stub implementation. In a real system, this would connect to Bing's API.",
            "source": "bing"
        }]