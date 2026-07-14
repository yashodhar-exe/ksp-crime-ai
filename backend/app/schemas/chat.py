from datetime import datetime

from pydantic import BaseModel


class ChatQueryRequest(BaseModel):
    session_id: str | None = None
    question: str


class ChatSource(BaseModel):
    case_id: str
    fir_number: str
    snippet: str


class ChatQueryResponse(BaseModel):
    session_id: str
    answer: str
    sources: list[ChatSource] = []


class ChatMessageOut(BaseModel):
    role: str  # "user" | "assistant"
    content: str
    timestamp: datetime


class ChatHistoryOut(BaseModel):
    session_id: str
    messages: list[ChatMessageOut]


class ChatExportRequest(BaseModel):
    session_id: str
