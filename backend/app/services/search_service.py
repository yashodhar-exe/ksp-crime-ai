from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case_master import CaseMaster

def search_entity(db: Session, *, entity_type: Optional[str], value: str) -> list[tuple[None, CaseMaster]]:
    """
    Mocked search for now as the SearchIndex table is no longer used in the new schema.
    """
    stmt = (
        select(CaseMaster)
        .where(CaseMaster.crime_no.ilike(f"%{value}%"))
        .limit(10)
    )
    return [(None, row) for row in db.execute(stmt).scalars()]


def find_by_fir(db: Session, fir_number: str) -> Optional[CaseMaster]:
    stmt = select(CaseMaster).where(CaseMaster.crime_no == fir_number)
    return db.execute(stmt).scalar_one_or_none()
