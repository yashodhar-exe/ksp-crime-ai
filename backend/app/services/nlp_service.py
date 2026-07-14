"""
Bridges chat.py routes to the ai/ layer described in ai/README.md
(rag/, chatbot/nl_to_sql.py, etc). That layer isn't implemented yet, so
this module ships a working fallback — Postgres full-text search over
`cases.complaint_text` (the GIN index schema.sql already creates for this
purpose) — so /chat/query returns real, grounded answers today instead of
a placeholder. Swap `_fallback_answer` for a call into ai/rag once that
pipeline exists; the ChatQueryResponse contract (answer + sources) is
already what a RAG response would look like.
"""
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.models.case import Case
from app.schemas.chat import ChatQueryResponse, ChatSource


def _fallback_answer(db: Session, question: str, session_id: str) -> ChatQueryResponse:
    tsquery = func.plainto_tsquery("english", question)
    stmt = (
        select(Case)
        .where(func.to_tsvector("english", Case.complaint_text).op("@@")(tsquery))
        .limit(5)
    )
    matches = db.execute(stmt).scalars().all()

    if not matches:
        return ChatQueryResponse(
            session_id=session_id,
            answer="I couldn't find any cases matching that question in the complaint narratives.",
            sources=[],
        )

    summary_lines = [f"Found {len(matches)} case(s) related to your question:"]
    sources = []
    for case in matches:
        summary_lines.append(f"- {case.fir_number} ({case.crime_type}, {case.status}, {case.district})")
        sources.append(
            ChatSource(
                case_id=case.case_id,
                fir_number=case.fir_number,
                snippet=case.complaint_text[:280],
            )
        )

    return ChatQueryResponse(session_id=session_id, answer="\n".join(summary_lines), sources=sources)


def answer_question(db: Session, question: str, session_id: str) -> ChatQueryResponse:
    if settings.OPENAI_OR_LLM_API_KEY and settings.VECTOR_DB_URL:
        # TODO: call into ai/rag once the embedding pipeline + vector store
        # exist (ai/rag/vector_store/). Left unimplemented on purpose so we
        # don't silently pretend to call an LLM that isn't wired up.
        pass
    return _fallback_answer(db, question, session_id)
