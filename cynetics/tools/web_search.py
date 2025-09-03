import requests
from cynetics.tools.base import BaseTool

class WebSearchTool(BaseTool):
    """A simple web search tool using DuckDuckGo."""
    
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Perform web searches using DuckDuckGo."
        )

    def run(self, query: str, max_results: int = 5) -> dict:
        """Perform a web search.
        
        Args:
            query: The search query.
            max_results: Maximum number of results to return.
            
        Returns:
            A dictionary with the search results.
        """
        try:
            # Using DuckDuckGo Instant Answer API
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
            
            # Extract relevant information
            results = {
                "status": "success",
                "query": query,
                "abstract": data.get("AbstractText", ""),
                "related_topics": []
            }
            
            # Get related topics
            related_topics = data.get("RelatedTopics", [])
            for topic in related_topics[:max_results]:
                if "FirstURL" in topic and "Text" in topic:
                    results["related_topics"].append({
                        "title": topic["Text"],
                        "url": topic["FirstURL"]
                    })
            
            return results
        except Exception as e:
            return {"status": "error", "message": str(e)}