from typing import Optional

from pydantic import BaseModel


class QueryPrompt(BaseModel):
    prompt: str
    workspace: Optional[str] = None


class GeneratedQuery(BaseModel):
    query: str
    confidence: float
