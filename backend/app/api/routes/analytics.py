from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.analytics import CrimeTrendPoint, CrimeTrendsOut, HotspotOut, CrimeHeadOut
from app.services import analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/crime-trends", response_model=CrimeTrendsOut)
def crime_trends(
    district: Optional[str] = None,
    period: str = Query(default="month", pattern="^(month|year)$"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> CrimeTrendsOut:
    rows = analytics_service.crime_trends(db, district=district, period=period)
    points = [CrimeTrendPoint(period=p, crime_group_name=ct, count=c) for p, ct, c in rows]
    return CrimeTrendsOut(district=district, period=period, points=points)


@router.get("/hotspots", response_model=list[HotspotOut])
def hotspots(
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[HotspotOut]:
    # District-level only — no GPS coordinates in the MVP dataset (see root README).
    rows = analytics_service.district_hotspots(db, limit=limit)
    return [
        HotspotOut(
            district_name=district,
            case_count=count,
            top_crime_group_name=None,
        )
        for district, count in rows
    ]


@router.get("/crime-heads", response_model=list[CrimeHeadOut])
def crime_heads(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[CrimeHeadOut]:
    rows = analytics_service.crime_heads_summary(db)
    return [
        CrimeHeadOut(
            crime_head_id=r[0],
            crime_group_name=r[1],
            case_count=r[2],
        )
        for r in rows
    ]
