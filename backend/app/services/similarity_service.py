from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.case_master import CaseMaster
from app.models.lookups import Unit


def find_similar_cases(db: Session, case: CaseMaster, limit: int = 10) -> list[tuple[CaseMaster, str]]:
    """
    MVP similarity: same crime_major_head_id always qualifies.
    """
    results: list[tuple[CaseMaster, str]] = []

    stmt = (
        select(CaseMaster)
        .options(
            joinedload(CaseMaster.police_station).joinedload(Unit.district),
            joinedload(CaseMaster.case_status),
            joinedload(CaseMaster.crime_major_head),
            joinedload(CaseMaster.crime_minor_head),
            joinedload(CaseMaster.case_category),
            joinedload(CaseMaster.gravity_offence)
        )
        .where(CaseMaster.crime_major_head_id == case.crime_major_head_id, CaseMaster.case_master_id != case.case_master_id)
        .limit(limit)
    )
    for c in db.execute(stmt).scalars().all():
        results.append((c, "Same crime type"))

    return results
