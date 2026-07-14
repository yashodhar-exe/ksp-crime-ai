from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.case import Case
from app.models.citizen import Citizen
from app.models.officer import Officer


def summary(db: Session, *, scoped_district: str | None) -> dict:
    """
    Card-level counts for a dashboard home screen. Citizen/officer totals
    are org-wide (those tables aren't district-scoped in schema.sql the
    way cases are), case counts respect the caller's district scope from
    core.rbac.scoped_district — same rule cases.py list_cases uses.
    """
    case_stmt = select(func.count()).select_from(Case)
    open_stmt = select(func.count()).select_from(Case).where(Case.status.in_(["Open", "Under Investigation", "Pending"]))
    critical_stmt = select(func.count()).select_from(Case).where(Case.priority == "Critical")

    if scoped_district:
        case_stmt = case_stmt.where(Case.district == scoped_district)
        open_stmt = open_stmt.where(Case.district == scoped_district)
        critical_stmt = critical_stmt.where(Case.district == scoped_district)

    return {
        "total_cases": db.execute(case_stmt).scalar_one(),
        "open_cases": db.execute(open_stmt).scalar_one(),
        "critical_cases": db.execute(critical_stmt).scalar_one(),
        "total_citizens": db.execute(select(func.count()).select_from(Citizen)).scalar_one(),
        "total_officers": db.execute(select(func.count()).select_from(Officer)).scalar_one(),
        "district": scoped_district,  # None means "all districts" (admin/SP)
    }


def status_breakdown(db: Session, *, scoped_district: str | None) -> list[tuple[str, int]]:
    stmt = select(Case.status, func.count().label("count")).group_by(Case.status)
    if scoped_district:
        stmt = stmt.where(Case.district == scoped_district)
    return [(row.status, row.count) for row in db.execute(stmt)]


def crime_type_breakdown(db: Session, *, scoped_district: str | None, limit: int = 8) -> list[tuple[str, int]]:
    stmt = select(Case.crime_type, func.count().label("count")).group_by(Case.crime_type).order_by(func.count().desc()).limit(limit)
    if scoped_district:
        stmt = stmt.where(Case.district == scoped_district)
    return [(row.crime_type, row.count) for row in db.execute(stmt)]


def recent_cases(db: Session, *, scoped_district: str | None, limit: int = 10) -> list[Case]:
    stmt = select(Case).order_by(Case.registered_date.desc()).limit(limit)
    if scoped_district:
        stmt = stmt.where(Case.district == scoped_district)
    return list(db.execute(stmt).scalars().all())


def recent_activity(db: Session, *, user_id: str | None, limit: int = 20) -> list[AuditLog]:
    """user_id=None returns org-wide activity (callers should gate that to admin/SP)."""
    stmt = select(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit)
    if user_id:
        stmt = stmt.where(AuditLog.user_id == user_id)
    return list(db.execute(stmt).scalars().all())
