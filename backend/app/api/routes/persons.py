"""
The PDF ER diagram has no central "citizen" master — Accused, Victim, and
ComplainantDetails are each scoped to a single case. This router provides
name-based lookup across those three tables (the practical equivalent of
"look up everything about this person") instead of a single citizen_id
lookup that the schema doesn't support.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.accused import Accused
from app.models.user import User
from app.models.case_master import CaseMaster
from app.models.complainant import ComplainantDetails
from app.models.lookups import CaseStatusMaster, CrimeSubHead
from app.models.victim import Victim
from app.schemas.persons import CoAccusedOut, PersonCaseLinkOut, PersonSearchResponse

router = APIRouter(prefix="/persons", tags=["persons"])


def _case_display(db: Session, case: CaseMaster) -> tuple[str | None, str | None]:
    sub_head = db.get(CrimeSubHead, case.crime_minor_head_id) if case.crime_minor_head_id else None
    status_row = db.get(CaseStatusMaster, case.case_status_id)
    return (
        sub_head.crime_head_name if sub_head else None,
        status_row.case_status_name if status_row else None,
    )


@router.get("/search", response_model=PersonSearchResponse)
def search_persons(
    q: str = Query(..., min_length=2, description="Name to search for (partial match)"),
    limit: int = Query(default=50, le=200),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> PersonSearchResponse:
    results: list[PersonCaseLinkOut] = []
    like = f"%{q}%"

    accused_stmt = (
        select(Accused, CaseMaster)
        .join(CaseMaster, Accused.case_master_id == CaseMaster.case_master_id)
        .where(Accused.accused_name.ilike(like))
        .limit(limit)
    )
    for accused, case in db.execute(accused_stmt):
        sub_head_name, status_name = _case_display(db, case)
        results.append(PersonCaseLinkOut(
            case_master_id=case.case_master_id, crime_no=case.crime_no,
            crime_sub_head_name=sub_head_name, case_status_name=status_name,
            role="Accused", person_name=accused.accused_name, age_year=accused.age_year,
        ))

    victim_stmt = (
        select(Victim, CaseMaster)
        .join(CaseMaster, Victim.case_master_id == CaseMaster.case_master_id)
        .where(Victim.victim_name.ilike(like))
        .limit(limit)
    )
    for victim, case in db.execute(victim_stmt):
        sub_head_name, status_name = _case_display(db, case)
        results.append(PersonCaseLinkOut(
            case_master_id=case.case_master_id, crime_no=case.crime_no,
            crime_sub_head_name=sub_head_name, case_status_name=status_name,
            role="Victim", person_name=victim.victim_name, age_year=victim.age_year,
        ))

    complainant_stmt = (
        select(ComplainantDetails, CaseMaster)
        .join(CaseMaster, ComplainantDetails.case_master_id == CaseMaster.case_master_id)
        .where(ComplainantDetails.complainant_name.ilike(like))
        .limit(limit)
    )
    for complainant, case in db.execute(complainant_stmt):
        sub_head_name, status_name = _case_display(db, case)
        results.append(PersonCaseLinkOut(
            case_master_id=case.case_master_id, crime_no=case.crime_no,
            crime_sub_head_name=sub_head_name, case_status_name=status_name,
            role="Complainant", person_name=complainant.complainant_name, age_year=complainant.age_year,
        ))

    return PersonSearchResponse(query=q, results=results[:limit])


@router.get("/co-accused", response_model=list[CoAccusedOut])
def co_accused_of(
    name: str = Query(..., min_length=2, description="Exact accused name to find repeat co-appearances for"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[CoAccusedOut]:
    """
    Repeat-offender-style lookup: finds every OTHER accused person whose
    name also appears in cases where `name` was accused, i.e. plausible
    co-accused / associates across multiple FIRs. This is the closest
    honest analog to the old "criminal network" feature, given the schema
    has no explicit relationship table between accused persons.
    """
    case_ids_stmt = select(Accused.case_master_id).where(Accused.accused_name == name)
    case_ids = [row[0] for row in db.execute(case_ids_stmt)]
    if not case_ids:
        return []

    co_stmt = (
        select(Accused.accused_name, func.count(func.distinct(Accused.case_master_id)).label("case_count"))
        .where(Accused.case_master_id.in_(case_ids), Accused.accused_name != name)
        .group_by(Accused.accused_name)
        .order_by(func.count(func.distinct(Accused.case_master_id)).desc())
        .limit(50)
    )

    out = []
    for co_name, case_count in db.execute(co_stmt):
        shared_stmt = select(Accused.case_master_id).where(
            Accused.accused_name == co_name, Accused.case_master_id.in_(case_ids)
        )
        shared = [row[0] for row in db.execute(shared_stmt)]
        out.append(CoAccusedOut(accused_name=co_name, shared_case_master_ids=shared, case_count=case_count))
    return out
