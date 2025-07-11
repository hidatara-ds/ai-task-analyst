from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class Workspace(BaseModel):
    id: int
    name: str


class ExportRequest(BaseModel):
    workspace: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    only_leads: bool = False


class Chat(BaseModel):
    session_id: str
    created_at_local: Optional[datetime]
    name: Optional[str]
    email: Optional[str]
    prompt: str
    response: str
    workspace_name: str
    workspace_id: int
