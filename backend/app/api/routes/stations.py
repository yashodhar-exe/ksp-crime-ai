from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.case_master import CaseMaster
from app.models.lookups import Unit
from app.models.user import User
from app.schemas.case import CaseOut

router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("")
def list_stations(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    stmt = select(Unit).options(joinedload(Unit.district), joinedload(Unit.unit_type)).order_by(Unit.unit_name)
    units = db.execute(stmt).scalars().all()
    return [
        {
            "unit_id": u.unit_id,
            "unit_name": u.unit_name,
            "unit_type_name": u.unit_type.unit_type_name if u.unit_type else "Unknown",
            "district_name": u.district.district_name if u.district else None,
            "active": u.active,
        }
        for u in units
    ]


@router.get("/{station_id}/cases", response_model=list[CaseOut])
def get_station_cases(station_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[CaseOut]:
    station = db.get(Unit, station_id)
    if station is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")
    stmt = select(CaseMaster).where(CaseMaster.police_station_id == station_id).order_by(CaseMaster.crime_registered_date.desc())
    return db.execute(stmt).scalars().all()
