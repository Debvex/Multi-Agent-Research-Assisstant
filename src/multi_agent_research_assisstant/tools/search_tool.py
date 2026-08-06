from typing import Type, List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import os

try:
    import requests
except Exception:
    requests = None


class SearchInput(BaseModel):
    query: str = Field(..., description="Search query string")
    top_k: int = Field(5, description="Number of results to return")


class SearchTool(BaseTool):
    name: str = "search_tool"
    description: str = "Performs web searches using Serper (google.serper.dev) and returns top sources with snippets."
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str, top_k: int = 5) -> str:
        api_key = os.environ.get("SERPER_API_KEY")
        if not requests:
            return "error: requests not installed; install requests to enable Serper integration"
        if not api_key:
            return "error: SERPER_API_KEY not set in environment"

        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        payload = {"q": query, "num": top_k}
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            return f"error: Serper request failed: {e}"

        results: List[str] = []
        # Serper returns 'organic' results with title, link, snippet
        organic = data.get("organic", [])
        for i, item in enumerate(organic[:top_k], start=1):
            title = item.get("title") or item.get("heading") or "(no title)"
            link = item.get("link") or item.get("url") or "(no url)"
            snippet = item.get("snippet") or item.get("description") or ""
            results.append(f"{i}. {title} - {link}\n   {snippet}")

        if not results:
            return "No results found (Serper returned empty)."
        return "\n\n".join(results)
