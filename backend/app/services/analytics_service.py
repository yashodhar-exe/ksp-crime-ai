from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.case import Case
from app.models.crime_pattern import CrimePattern


def crime_trends(db: Session, *, district: str | None, period: str) -> list[tuple[str, str, int]]:
    """
    period is 'month' or 'year' — grouped via Postgres date_trunc. Returns
    (period_label, crime_type, count) tuples; the route layer formats them
    into CrimeTrendPoint.
    """
    trunc_unit = "year" if period == "year" else "month"
    period_col = func.to_char(func.date_trunc(trunc_unit, Case.incident_date), "YYYY-MM" if trunc_unit == "month" else "YYYY")

    stmt = select(period_col.label("period"), Case.crime_type, func.count().label("count"))
    if district:
        stmt = stmt.where(Case.district == district)
    stmt = stmt.group_by(period_col, Case.crime_type).order_by(period_col)

    return [(row.period, row.crime_type, row.count) for row in db.execute(stmt)]


def district_hotspots(db: Session, *, limit: int = 20) -> list[tuple[str, int]]:
    """District-level case counts — no GPS data in the MVP dataset (see root README)."""
    stmt = (
        select(Case.district, func.count().label("count"))
        .group_by(Case.district)
        .order_by(func.count().desc())
        .limit(limit)
    )
    return [(row.district, row.count) for row in db.execute(stmt)]


def top_crime_type_for_district(db: Session, district: str) -> str | None:
    stmt = (
        select(Case.crime_type, func.count().label("count"))
        .where(Case.district == district)
        .group_by(Case.crime_type)
        .order_by(func.count().desc())
        .limit(1)
    )
    row = db.execute(stmt).first()
    return row.crime_type if row else None


def pattern_summaries(db: Session) -> list[tuple[CrimePattern, int]]:
    stmt = (
        select(CrimePattern, func.count(Case.case_id).label("case_count"))
        .outerjoin(Case, Case.pattern_id == CrimePattern.pattern_id)
        .group_by(CrimePattern.pattern_id)
        .order_by(func.count(Case.case_id).desc())
    )
    return [(row[0], row[1]) for row in db.execute(stmt)]
