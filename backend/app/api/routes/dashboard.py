from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.rbac import has_permission, scoped_district
from app.db.session import get_db
from app.models.user import User
from app.schemas.dashboard import (
    BreakdownPoint,
    DashboardActivityOut,
    DashboardRecentOut,
    DashboardStatsOut,
    DashboardSummaryOut,
)
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _caller_district(current_user: User) -> str | None:
    user_district = current_user.station.district if current_user.station else None
    return scoped_district(current_user.role, user_district)


@router.get("/summary", response_model=DashboardSummaryOut)
def get_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> DashboardSummaryOut:
    district = _caller_district(current_user)
    return DashboardSummaryOut(**dashboard_service.summary(db, scoped_district=district))


@router.get("/stats", response_model=DashboardStatsOut)
def get_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> DashboardStatsOut:
    district = _caller_district(current_user)
    return DashboardStatsOut(
        by_status=[BreakdownPoint(label=s, count=c) for s, c in dashboard_service.status_breakdown(db, scoped_district=district)],
        by_crime_type=[
            BreakdownPoint(label=ct, count=c) for ct, c in dashboard_service.crime_type_breakdown(db, scoped_district=district)
        ],
    )


@router.get("/recent", response_model=DashboardRecentOut)
def get_recent(
    limit: int = Query(default=10, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardRecentOut:
    district = _caller_district(current_user)
    cases = dashboard_service.recent_cases(db, scoped_district=district, limit=limit)
    return DashboardRecentOut(cases=cases)


@router.get("/activity", response_model=DashboardActivityOut)
def get_activity(
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardActivityOut:
    # Non-privileged users see their own activity only; admin/SP
    # (can_view_all_districts) see the org-wide feed — mirrors the
    # district-scoping rule used elsewhere rather than introducing a new
    # permission just for this endpoint.
    user_id = None if has_permission(current_user.role, "can_view_all_districts") else current_user.user_id
    entries = dashboard_service.recent_activity(db, user_id=user_id, limit=limit)
    return DashboardActivityOut(entries=entries)
