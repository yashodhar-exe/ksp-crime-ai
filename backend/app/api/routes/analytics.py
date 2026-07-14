from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.analytics import CrimeTrendPoint, CrimeTrendsOut, HotspotOut, PatternSummaryOut
from app.services import analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/crime-trends", response_model=CrimeTrendsOut)
def crime_trends(
    district: str | None = None,
    period: str = Query(default="month", pattern="^(month|year)$"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> CrimeTrendsOut:
    rows = analytics_service.crime_trends(db, district=district, period=period)
    points = [CrimeTrendPoint(period=p, crime_type=ct, count=c) for p, ct, c in rows]
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
            district=district,
            case_count=count,
            top_crime_type=analytics_service.top_crime_type_for_district(db, district),
        )
        for district, count in rows
    ]


@router.get("/patterns", response_model=list[PatternSummaryOut])
def patterns(db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[PatternSummaryOut]:
    rows = analytics_service.pattern_summaries(db)
    return [
        PatternSummaryOut(
            pattern_id=pattern.pattern_id,
            crime_type=pattern.crime_type,
            modus_operandi=pattern.modus_operandi,
            risk_level=pattern.risk_level,
            case_count=count,
        )
        for pattern, count in rows
    ]
