from typing import Type, List, Tuple
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import os
import glob
import re


class RAGRetrieveInput(BaseModel):
    query: str = Field(..., description="Query to retrieve from the local knowledge base")
    top_k: int = Field(5, description="Number of passages to return")


def _score_text(query: str, text: str) -> int:
    # simple scoring: count overlapping words
    q_words = set(re.findall(r"\w+", query.lower()))
    t_words = set(re.findall(r"\w+", text.lower()))
    return len(q_words & t_words)


class RAGRetriever(BaseTool):
    name: str = "rag_retriever"
    description: str = "Retrieves relevant passages from local knowledge/memory stores by simple overlap scoring."
    args_schema: Type[BaseModel] = RAGRetrieveInput

    def _run(self, query: str, top_k: int = 5) -> str:
        kb_dir = os.path.join(os.getcwd(), "knowledge")
        if not os.path.isdir(kb_dir):
            return "error: knowledge directory not found"

        candidates: List[Tuple[int, str, str]] = []  # (score, filename, excerpt)
        for path in glob.glob(os.path.join(kb_dir, "**"), recursive=True):
            if os.path.isdir(path):
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                continue
            # split into 1000-char passages
            passages = [content[i:i+1000] for i in range(0, len(content), 1000)]
            for p in passages:
                score = _score_text(query, p)
                if score > 0:
                    candidates.append((score, os.path.basename(path), p.strip()))

        candidates.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, fname, excerpt in candidates[:top_k]:
            results.append(f"File: {fname} (score={score})\n{excerpt[:500]}...")

        if not results:
            return "No relevant passages found in local knowledge."
        return "\n\n".join(results)
