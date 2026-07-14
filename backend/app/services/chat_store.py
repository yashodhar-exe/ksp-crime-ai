"""
schema.sql has no chat_sessions/chat_messages tables — the chatbot is
scoped as an MVP feature layered on top of the existing case data (see
ai/README.md). This in-process store is enough for a demo/single-instance
deployment. For multi-worker or persistent history, replace this with a
`chat_sessions` / `chat_messages` table and point chat.py at a real
service instead of this module — the ChatHistoryOut/ChatMessageOut schemas
already match what that table would return.
"""
import uuid
from datetime import datetime, timezone

_SESSIONS: dict[str, list[dict]] = {}


def new_session_id() -> str:
    return f"SESSION{uuid.uuid4().hex[:10].upper()}"


def append_message(session_id: str, role: str, content: str) -> None:
    _SESSIONS.setdefault(session_id, []).append(
        {"role": role, "content": content, "timestamp": datetime.now(timezone.utc).replace(tzinfo=None)}
    )


def get_history(session_id: str) -> list[dict]:
    return _SESSIONS.get(session_id, [])
