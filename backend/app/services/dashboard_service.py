from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.models.audit_log import AuditLog
from app.models.case_master import CaseMaster
from app.models.employee import Employee
from app.models.victim import Victim
from app.models.accused import Accused
from app.models.lookups import CaseStatusMaster, CrimeHead, Unit, District


def summary(db: Session, *, scoped_district: str | None) -> dict:
    """
    Card-level counts for a dashboard home screen.
    """
    # Total Cases
    case_stmt = select(func.count()).select_from(CaseMaster)
    
    # Open Cases (1: Under Investigation, 7: Pending Trial)
    open_stmt = select(func.count()).select_from(CaseMaster).where(CaseMaster.case_status_id.in_([1, 7]))
    
    # Critical Cases (Heinous -> 1)
    critical_stmt = select(func.count()).select_from(CaseMaster).where(CaseMaster.gravity_offence_id == 1)

    if scoped_district:
        # Join Unit and District to filter by district_name
        district_join = (Unit, CaseMaster.police_station_id == Unit.unit_id)
        state_district_join = (District, Unit.district_id == District.district_id)
        
        case_stmt = case_stmt.join(*district_join).join(*state_district_join).where(District.district_name == scoped_district)
        open_stmt = open_stmt.join(*district_join).join(*state_district_join).where(District.district_name == scoped_district)
        critical_stmt = critical_stmt.join(*district_join).join(*state_district_join).where(District.district_name == scoped_district)

    # Total Citizens (Victims + Accused)
    total_victims = db.execute(select(func.count()).select_from(Victim)).scalar_one()
    total_accused = db.execute(select(func.count()).select_from(Accused)).scalar_one()
    total_citizens = total_victims + total_accused

    # Total Officers (Employees)
    total_officers = db.execute(select(func.count()).select_from(Employee)).scalar_one()

    return {
        "total_cases": db.execute(case_stmt).scalar_one(),
        "open_cases": db.execute(open_stmt).scalar_one(),
        "critical_cases": db.execute(critical_stmt).scalar_one(),
        "total_citizens": total_citizens,
        "total_officers": total_officers,
        "district": scoped_district,  # None means "all districts" (admin/SP)
    }


def status_breakdown(db: Session, *, scoped_district: str | None) -> list[tuple[str, int]]:
    stmt = (
        select(CaseStatusMaster.case_status_name, func.count(CaseMaster.case_master_id).label("count"))
        .join(CaseMaster, CaseStatusMaster.case_status_id == CaseMaster.case_status_id)
        .group_by(CaseStatusMaster.case_status_name)
    )
    if scoped_district:
        stmt = stmt.join(Unit, CaseMaster.police_station_id == Unit.unit_id).join(District, Unit.district_id == District.district_id).where(District.district_name == scoped_district)
    return [(row.case_status_name, row.count) for row in db.execute(stmt)]


def crime_type_breakdown(db: Session, *, scoped_district: str | None, limit: int = 8) -> list[tuple[str, int]]:
    stmt = (
        select(CrimeHead.crime_group_name, func.count(CaseMaster.case_master_id).label("count"))
        .join(CaseMaster, CrimeHead.crime_head_id == CaseMaster.crime_major_head_id)
        .group_by(CrimeHead.crime_group_name)
        .order_by(func.count(CaseMaster.case_master_id).desc())
        .limit(limit)
    )
    if scoped_district:
        stmt = stmt.join(Unit, CaseMaster.police_station_id == Unit.unit_id).join(District, Unit.district_id == District.district_id).where(District.district_name == scoped_district)
    return [(row.crime_group_name, row.count) for row in db.execute(stmt)]


def recent_cases(db: Session, *, scoped_district: str | None, limit: int = 10) -> list[CaseMaster]:
    stmt = (
        select(CaseMaster)
        .options(
            joinedload(CaseMaster.police_station).joinedload(Unit.district),
            joinedload(CaseMaster.case_status),
            joinedload(CaseMaster.crime_major_head),
            joinedload(CaseMaster.gravity_offence),
        )
        .order_by(CaseMaster.crime_registered_date.desc())
        .limit(limit)
    )
    if scoped_district:
        stmt = stmt.join(Unit, CaseMaster.police_station_id == Unit.unit_id).join(District, Unit.district_id == District.district_id).where(District.district_name == scoped_district)
    return list(db.execute(stmt).scalars().all())


def recent_activity(db: Session, *, user_id: str | None, limit: int = 20) -> list[AuditLog]:
    stmt = select(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit)
    if user_id:
        stmt = stmt.where(AuditLog.user_id == user_id)
    return list(db.execute(stmt).scalars().all())
