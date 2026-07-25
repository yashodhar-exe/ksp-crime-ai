from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.case_master import CaseMaster
from app.models.lookups import CrimeHead, CaseStatusMaster, Unit, District


def list_cases(
    db: Session,
    *,
    crime_type: str | None = None,
    status: str | None = None,
    district: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    scoped_district: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[CaseMaster], int]:
    stmt = select(CaseMaster)

    # Need joins if we're filtering by lookup strings
    if crime_type:
        stmt = stmt.join(CrimeHead, CaseMaster.crime_major_head_id == CrimeHead.crime_head_id).where(CrimeHead.crime_group_name == crime_type)
    if status:
        stmt = stmt.join(CaseStatusMaster, CaseMaster.case_status_id == CaseStatusMaster.case_status_id).where(CaseStatusMaster.case_status_name == status)
    
    # We may need District join if district or scoped_district is provided
    needs_district_join = bool(district or scoped_district)
    if needs_district_join:
        stmt = stmt.join(Unit, CaseMaster.police_station_id == Unit.unit_id).join(District, Unit.district_id == District.district_id)
        if district:
            stmt = stmt.where(District.district_name == district)
        if scoped_district:
            stmt = stmt.where(District.district_name == scoped_district)

    if date_from:
        stmt = stmt.where(CaseMaster.incident_from_date >= date_from)
    if date_to:
        stmt = stmt.where(CaseMaster.incident_to_date <= date_to)

    total = len(db.execute(stmt).scalars().all())
    
    # Add joinedloads for Pydantic schema serialization
    stmt = stmt.options(
        joinedload(CaseMaster.police_station).joinedload(Unit.district),
        joinedload(CaseMaster.case_status),
        joinedload(CaseMaster.crime_major_head),
        joinedload(CaseMaster.crime_minor_head),
        joinedload(CaseMaster.case_category),
        joinedload(CaseMaster.gravity_offence)
    )
    
    stmt = stmt.order_by(CaseMaster.crime_registered_date.desc()).limit(limit).offset(offset)
    items = db.execute(stmt).scalars().unique().all()
    return list(items), total


def get_case(db: Session, case_master_id: int) -> CaseMaster | None:
    return db.query(CaseMaster).options(
        joinedload(CaseMaster.police_station).joinedload(Unit.district),
        joinedload(CaseMaster.case_status),
        joinedload(CaseMaster.crime_major_head),
        joinedload(CaseMaster.crime_minor_head),
        joinedload(CaseMaster.case_category),
        joinedload(CaseMaster.gravity_offence),
        joinedload(CaseMaster.complainants),
        joinedload(CaseMaster.victims),
        joinedload(CaseMaster.accused),
        joinedload(CaseMaster.act_sections),
        joinedload(CaseMaster.arrest_surrenders),
        joinedload(CaseMaster.chargesheets),
        joinedload(CaseMaster.registering_officer),
        joinedload(CaseMaster.court)
    ).filter(CaseMaster.case_master_id == case_master_id).first()


def create_case(db: Session, case_id: str, data: dict) -> CaseMaster:
    # Creating cases via API is complex with CaseMaster.
    # Leaving placeholder or throwing not implemented as we didn't specify case creation in migration.
    raise NotImplementedError("Creating cases is not supported via this API yet.")


def update_case(db: Session, case: CaseMaster, data: dict) -> CaseMaster:
    for field, value in data.items():
        if value is not None and hasattr(case, field):
            setattr(case, field, value)
    db.commit()
    db.refresh(case)
    return case
