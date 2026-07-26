import io

from fastapi import APIRouter, Depends, HTTPException, Request, status, Form
from fastapi.responses import StreamingResponse
from typing import Optional
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.chat import (
    ChatExportRequest,
    ChatHistoryOut,
    ChatMessageOut,
    ChatQueryRequest,
    ChatQueryResponse,
)
from app.services import chat_store, nlp_service
from app.services.audit_service import log_action

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/query", response_model=ChatQueryResponse)
def chat_query(
    request: Request,
    question: str = Form(...),
    session_id: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChatQueryResponse:
    session_id = session_id or chat_store.new_session_id()

    chat_store.append_message(session_id, "user", question)
    response = nlp_service.answer_question(db, question, session_id)
    chat_store.append_message(session_id, "assistant", response.answer)

    log_action(
        db,
        user_id=current_user.user_id,
        action="Viewed Case" if response.sources else "Searched Entity",
        case_id=response.sources[0].case_id if response.sources else None,
        ip_address=request.client.host if request.client else "unknown",
    )

    return response


@router.get("/history/{session_id}", response_model=ChatHistoryOut)
def chat_history(session_id: str, _: User = Depends(get_current_user)) -> ChatHistoryOut:
    messages = chat_store.get_history(session_id)
    if not messages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such chat session")
    return ChatHistoryOut(
        session_id=session_id,
        messages=[ChatMessageOut(role=m["role"], content=m["content"], timestamp=m["timestamp"]) for m in messages],
    )


@router.post("/export")
def chat_export(
    request: Request,
    session_id: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> StreamingResponse:
    messages = chat_store.get_history(session_id)
    if not messages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such chat session")

    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "KSP Crime AI - Chat Transcript", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, f"Session: {session_id}", ln=True)
    pdf.ln(4)

    for m in messages:
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 6, f"[{m['timestamp'].strftime('%Y-%m-%d %H:%M')}] {m['role'].upper()}")
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, m["content"])
        pdf.ln(2)

    buffer = io.BytesIO(pdf.output(dest="S"))
    buffer.seek(0)

    log_action(
        db,
        user_id=current_user.user_id,
        action="Downloaded Report",
        ip_address=request.client.host if request.client else "unknown",
    )

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="chat_{session_id}.pdf"'},
    )
