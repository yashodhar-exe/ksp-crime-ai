from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.case_master import CaseMaster
from app.models.lookups import CrimeHead, District, Unit


def crime_trends(db: Session, *, district: Optional[str], period: str) -> list[tuple[str, str, int]]:
    """
    period is 'month' or 'year' — grouped via Postgres date_trunc. Returns
    (period_label, crime_type, count) tuples; the route layer formats them
    into CrimeTrendPoint.
    """
    trunc_unit = "year" if period == "year" else "month"
    period_col = func.to_char(func.date_trunc(trunc_unit, CaseMaster.incident_from_date), "YYYY-MM" if trunc_unit == "month" else "YYYY")

    stmt = (
        select(period_col.label("period"), CrimeHead.crime_group_name, func.count().label("count"))
        .select_from(CaseMaster)
        .join(CrimeHead, CaseMaster.crime_major_head_id == CrimeHead.crime_head_id)
    )
    if district:
        stmt = stmt.join(Unit, CaseMaster.police_station_id == Unit.unit_id).join(District, Unit.district_id == District.district_id)
        stmt = stmt.where(District.district_name == district)
        
    stmt = stmt.group_by(period_col, CrimeHead.crime_group_name).order_by(period_col)

    return [(row.period, row.crime_group_name, row.count) for row in db.execute(stmt)]


def district_hotspots(db: Session, *, limit: int = 20) -> list[tuple[str, int]]:
    """District-level case counts — no GPS data in the MVP dataset (see root README)."""
    stmt = (
        select(District.district_name, func.count().label("count"))
        .select_from(CaseMaster)
        .join(Unit, CaseMaster.police_station_id == Unit.unit_id)
        .join(District, Unit.district_id == District.district_id)
        .group_by(District.district_name)
        .order_by(func.count().desc())
        .limit(limit)
    )
    return [(row.district_name, row.count) for row in db.execute(stmt)]


def top_crime_type_for_district(db: Session, district: str) -> Optional[str]:
    stmt = (
        select(CrimeHead.crime_group_name, func.count().label("count"))
        .select_from(CaseMaster)
        .join(CrimeHead, CaseMaster.crime_major_head_id == CrimeHead.crime_head_id)
        .join(Unit, CaseMaster.police_station_id == Unit.unit_id)
        .join(District, Unit.district_id == District.district_id)
        .where(District.district_name == district)
        .group_by(CrimeHead.crime_group_name)
        .order_by(func.count().desc())
        .limit(1)
    )
    row = db.execute(stmt).first()
    return row.crime_group_name if row else None


def crime_heads_summary(db: Session) -> list[tuple[int, str, int]]:
    stmt = (
        select(CrimeHead.crime_head_id, CrimeHead.crime_group_name, func.count(CaseMaster.case_master_id).label("count"))
        .outerjoin(CaseMaster, CrimeHead.crime_head_id == CaseMaster.crime_major_head_id)
        .group_by(CrimeHead.crime_head_id, CrimeHead.crime_group_name)
        .order_by(func.count(CaseMaster.case_master_id).desc())
    )
    return [(row.crime_head_id, row.crime_group_name, row.count) for row in db.execute(stmt)]
