from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import re


class SummariseInput(BaseModel):
    text: str = Field(..., description="Text to summarise")
    length: str = Field("short", description="short|medium|long|bullet")


def _split_sentences(text: str):
    # naive sentence splitter
    return re.split(r'(?<=[.!?])\s+', text.strip())


class SummariserTool(BaseTool):
    name: str = "summariser_tool"
    description: str = "Produces extractive summaries at multiple lengths from a source text."
    args_schema: Type[BaseModel] = SummariseInput

    def _run(self, text: str, length: str = "short") -> str:
        sents = _split_sentences(text)
        if not sents:
            return ""
        if length == "bullet":
            bullets = sents[:6]
            return "\n".join([f"- {b.strip()}" for b in bullets])
        if length == "long":
            return "\n\n".join(sents[:12])
        if length == "medium":
            return "\n\n".join(sents[:6])
        # short
        return sents[0]
