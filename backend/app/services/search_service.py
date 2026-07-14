from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case import Case
from app.models.search_index import SearchIndex


def search_entity(db: Session, *, entity_type: str | None, value: str) -> list[tuple[SearchIndex, Case]]:
    """
    Uses the (entity_type, entity_value) composite index defined in
    schema.sql. entity_value is matched with ILIKE so partial phone
    numbers / partial names still surface results.
    """
    stmt = (
        select(SearchIndex, Case)
        .join(Case, Case.case_id == SearchIndex.case_id)
        .where(SearchIndex.entity_value.ilike(f"%{value}%"))
    )
    if entity_type:
        stmt = stmt.where(SearchIndex.entity_type == entity_type)
    stmt = stmt.limit(100)

    return [(row[0], row[1]) for row in db.execute(stmt)]


def find_by_fir(db: Session, fir_number: str) -> Case | None:
    stmt = select(Case).where(Case.fir_number == fir_number)
    return db.execute(stmt).scalar_one_or_none()
