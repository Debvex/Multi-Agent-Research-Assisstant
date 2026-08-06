from typing import Type, List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import os
try:
    import requests
except Exception:
    requests = None


class FactCheckInput(BaseModel):
    text: str = Field(..., description="Text or claim to verify")


class FactChecker(BaseTool):
    name: str = "fact_checker"
    description: str = "Checks claims for verifiability using Serper search and returns issues or confirmation."
    args_schema: Type[BaseModel] = FactCheckInput

    def _run(self, text: str) -> str:
        # Use Serper search to find supporting or contradicting evidence
        api_key = os.environ.get("SERPER_API_KEY")
        if not requests:
            return "error: requests not installed; cannot perform online verification"
        if not api_key:
            return "error: SERPER_API_KEY not set in environment"

        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        payload = {"q": text, "num": 5}
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=12)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            return f"error: Serper request failed: {e}"

        organic = data.get("organic", [])
        if not organic:
            return "revise: no supporting sources found"

        # simple heuristic: if any snippet contains a key phrase from the claim, mark verified
        claim_words = set([w.lower() for w in text.split() if len(w) > 4])
        for item in organic:
            snippet = (item.get("snippet") or "").lower()
            snippet_words = set(snippet.split())
            overlap = len(claim_words & snippet_words)
            if overlap >= max(1, int(len(claim_words) * 0.15)):
                title = item.get("title") or item.get("heading") or item.get("link")
                link = item.get("link") or item.get("url")
                return f"verified: found supporting source - {title} - {link}"

        return "revise: no sufficient evidence found; consider adding citations"
