from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case import Case


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
) -> tuple[list[Case], int]:
    """
    scoped_district (from core.rbac.scoped_district) is applied in addition
    to any explicit `district` filter the caller passes, so an officer who
    can only see their own district can't override that by querying a
    different one.
    """
    stmt = select(Case)

    if crime_type:
        stmt = stmt.where(Case.crime_type == crime_type)
    if status:
        stmt = stmt.where(Case.status == status)
    if district:
        stmt = stmt.where(Case.district == district)
    if scoped_district:
        stmt = stmt.where(Case.district == scoped_district)
    if date_from:
        stmt = stmt.where(Case.incident_date >= date_from)
    if date_to:
        stmt = stmt.where(Case.incident_date <= date_to)

    total = len(db.execute(stmt).scalars().all())
    stmt = stmt.order_by(Case.registered_date.desc()).limit(limit).offset(offset)
    items = db.execute(stmt).scalars().all()
    return list(items), total


def get_case(db: Session, case_id: str) -> Case | None:
    return db.get(Case, case_id)


def create_case(db: Session, case_id: str, data: dict) -> Case:
    case = Case(case_id=case_id, **data)
    db.add(case)
    db.commit()
    db.refresh(case)
    return case


def update_case(db: Session, case: Case, data: dict) -> Case:
    for field, value in data.items():
        if value is not None:
            setattr(case, field, value)
    db.commit()
    db.refresh(case)
    return case
