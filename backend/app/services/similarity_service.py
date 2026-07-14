from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case import Case


def find_similar_cases(db: Session, case: Case, limit: int = 10) -> list[tuple[Case, str]]:
    """
    MVP similarity: same crime_type always qualifies; same pattern_id (when
    the source case has one) is a stronger signal and is returned first.
    This stands in for the "predictive analytics" scope note in the root
    README — full ML-based similarity can replace this function later
    without touching the route/schema layer.
    """
    results: list[tuple[Case, str]] = []

    if case.pattern_id:
        stmt = (
            select(Case)
            .where(Case.pattern_id == case.pattern_id, Case.case_id != case.case_id)
            .limit(limit)
        )
        for c in db.execute(stmt).scalars().all():
            results.append((c, "Same crime pattern"))

    if len(results) < limit:
        remaining = limit - len(results)
        seen_ids = {c.case_id for c, _ in results} | {case.case_id}
        stmt = (
            select(Case)
            .where(Case.crime_type == case.crime_type, Case.case_id.not_in(seen_ids))
            .limit(remaining)
        )
        for c in db.execute(stmt).scalars().all():
            results.append((c, "Same crime type"))

    return results
