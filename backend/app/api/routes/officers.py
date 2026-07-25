from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.case_master import CaseMaster
from app.models.employee import Employee
from app.models.user import User
from app.schemas.case import CaseOut
from app.schemas.officer import OfficerOut

router = APIRouter(prefix="/officers", tags=["officers"])


@router.get("/{officer_id}")
def get_officer(officer_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    officer = db.get(Employee, officer_id)
    if officer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Officer not found")
    
    return {
        "officer_id": str(officer.employee_id),
        "name": officer.employee_name,
        "rank": officer.rank.rank_name if officer.rank else "Unknown",
        "station_id": str(officer.unit_id) if officer.unit_id else "",
        "contact_number": officer.mobile_no or ""
    }


@router.get("/{officer_id}/cases", response_model=list[CaseOut])
def get_officer_cases(officer_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[CaseOut]:
    officer = db.get(Employee, officer_id)
    if officer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Officer not found")
    stmt = select(CaseMaster).where(CaseMaster.police_person_id == officer_id).order_by(CaseMaster.crime_registered_date.desc())
    return db.execute(stmt).scalars().all()
