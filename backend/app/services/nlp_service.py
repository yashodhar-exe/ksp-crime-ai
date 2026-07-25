"""
Bridges chat.py routes to the ai/ layer described in ai/README.md
"""
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.config import settings
from app.models.case_master import CaseMaster
from app.schemas.chat import ChatQueryResponse, ChatSource
from app.models.lookups import Unit, District, CrimeHead


def _fallback_answer(db: Session, question: str, session_id: str) -> ChatQueryResponse:
    # Full text search fallback - mock for now since complaint text was moved/removed in CaseMaster schema
    tsquery = func.plainto_tsquery("english", question)
    
    # We will just search crime group names instead as a fallback
    stmt = (
        select(CaseMaster)
        .options(
            joinedload(CaseMaster.police_station).joinedload(Unit.district),
            joinedload(CaseMaster.case_status),
            joinedload(CaseMaster.crime_major_head)
        )
        .join(CrimeHead, CaseMaster.crime_major_head_id == CrimeHead.crime_head_id)
        .where(func.to_tsvector("english", CrimeHead.crime_group_name).op("@@")(tsquery))
        .limit(5)
    )
    matches = db.execute(stmt).scalars().all()

    if not matches:
        return ChatQueryResponse(
            session_id=session_id,
            answer="I couldn't find any cases matching that question.",
            sources=[],
        )

    summary_lines = [f"Found {len(matches)} case(s) related to your question:"]
    sources = []
    for case in matches:
        crime_type = case.crime_head_name or "Unknown"
        status = case.case_status_name or "Unknown"
        district = case.police_station.district.district_name if case.police_station and case.police_station.district else "Unknown"
        
        summary_lines.append(f"- {case.crime_no} ({crime_type}, {status}, {district})")
        sources.append(
            ChatSource(
                case_id=str(case.case_master_id),
                fir_number=case.crime_no,
                snippet=crime_type,
            )
        )

    return ChatQueryResponse(session_id=session_id, answer="\n".join(summary_lines), sources=sources)


def answer_question(db: Session, question: str, session_id: str) -> ChatQueryResponse:
    if settings.OPENAI_OR_LLM_API_KEY and settings.VECTOR_DB_URL:
        # TODO: call into ai/rag once the embedding pipeline + vector store
        pass
    return _fallback_answer(db, question, session_id)
