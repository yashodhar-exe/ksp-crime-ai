from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.case import Case
from app.models.police_station import PoliceStation
from app.models.user import User
from app.schemas.case import CaseOut
from app.schemas.officer import StationOut

router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("", response_model=list[StationOut])
def list_stations(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[StationOut]:
    return db.execute(select(PoliceStation).order_by(PoliceStation.station_name)).scalars().all()


@router.get("/{station_id}/cases", response_model=list[CaseOut])
def get_station_cases(station_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[CaseOut]:
    station = db.get(PoliceStation, station_id)
    if station is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station not found")
    stmt = select(Case).where(Case.station_id == station_id).order_by(Case.registered_date.desc())
    return db.execute(stmt).scalars().all()
