from typing import Type, List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import datetime
import os

try:
    import requests
    import re
except Exception:
    requests = None
    re = None


class CitationInput(BaseModel):
    sources: List[str] = Field(..., description="List of source URLs or strings")


class CitationManager(BaseTool):
    name: str = "citation_manager"
    description: str = "Formats a list of sources into numbered citations and a References section, fetching titles when possible."
    args_schema: Type[BaseModel] = CitationInput

    def _fetch_title(self, url: str) -> str:
        if not requests:
            return "(title unavailable; requests missing)"
        try:
            r = requests.get(url, timeout=8)
            r.raise_for_status()
            html = r.text
            if re:
                m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
                if m:
                    return m.group(1).strip()
            return url
        except Exception:
            return url

    def _run(self, sources: list) -> str:
        lines = []
        for i, s in enumerate(sources, start=1):
            title = self._fetch_title(s) if s.startswith("http") else s
            lines.append(f"[{i}] {title} - {s} (accessed {datetime.date.today().isoformat()})")
        refs = "\n".join(lines)
        return f"References:\n{refs}"
