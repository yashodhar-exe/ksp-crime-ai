from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.case import Case
from app.models.officer import Officer
from app.models.user import User
from app.schemas.case import CaseOut
from app.schemas.officer import OfficerOut

router = APIRouter(prefix="/officers", tags=["officers"])


@router.get("/{officer_id}", response_model=OfficerOut)
def get_officer(officer_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> OfficerOut:
    officer = db.get(Officer, officer_id)
    if officer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Officer not found")
    return officer


@router.get("/{officer_id}/cases", response_model=list[CaseOut])
def get_officer_cases(officer_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[CaseOut]:
    officer = db.get(Officer, officer_id)
    if officer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Officer not found")
    stmt = select(Case).where(Case.officer_id == officer_id).order_by(Case.registered_date.desc())
    return db.execute(stmt).scalars().all()
