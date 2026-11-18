import os
from tavily import TavilyClient
from langchain_core.tools import tool
import requests


tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for information about a topic. Returns top results with titles, URLs and content snippets."""
    try:
        results = tavily_client.search(
            query=query,
            max_results=3,
            include_raw_content=False
        )
        output = []
        for r in results["results"]:
            output.append(f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['content']}\n")
        return "\n---\n".join(output)
    except Exception as e:
        return f"Search failed: {str(e)}"

@tool
def read_url(url: str) -> str:
    """Read the full content of a webpage. Use this to get detailed information from a specific URL found in search results."""
    try:
        result = tavily_client.extract(urls=[url])
        if result["results"]:
            content = result["results"][0]["raw_content"]
            # Trim to avoid token overflow
            return content[:1500] if len(content) > 1500 else content
        return "Could not extract content from URL."
    except Exception as e:
        return f"Could not read URL: {str(e)}"

@tool
def write_report(filename: str, content: str) -> str:
    """Save the final research report to a markdown file."""
    try:
        os.makedirs("reports", exist_ok=True)
        filepath = f"reports/{filename}.md"
        with open(filepath, "w") as f:
            f.write(content)
        return f"Report saved to {filepath}"
    except Exception as e:
        return f"Failed to save report: {str(e)}"

tools = [web_search, read_url, write_report]