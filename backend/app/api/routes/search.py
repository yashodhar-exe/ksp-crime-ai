from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.case import CaseDetailOut
from app.schemas.search import SearchResponse, SearchResultOut
from app.services import search_service
from app.services.audit_service import log_action

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=SearchResponse)
def search_entity(
    request: Request,
    value: str = Query(..., min_length=2),
    entity_type: Optional[str] = Query(default=None, description="Citizen | Phone | Vehicle | Bank | Officer | Case"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SearchResponse:
    rows = search_service.search_entity(db, entity_type=entity_type, value=value)

    log_action(
        db,
        user_id=current_user.user_id,
        action="Searched Entity",
        ip_address=request.client.host if request.client else "unknown",
    )

    results = [
        SearchResultOut(
            entity_type=idx.entity_type,
            entity_value=idx.entity_value,
            case_id=case.case_id,
            fir_number=case.fir_number,
            crime_type=case.crime_type,
            status=case.status,
        )
        for idx, case in rows
    ]
    return SearchResponse(query=value, entity_type=entity_type, results=results)


@router.get("/fir/{fir_number}", response_model=CaseDetailOut)
def search_by_fir(fir_number: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> CaseDetailOut:
    case = search_service.find_by_fir(db, fir_number)
    if case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No case found for that FIR number")

    detail = CaseDetailOut.model_validate(case)
    detail.station_name = case.station.station_name if case.station else None
    detail.officer_name = case.officer.name if case.officer else None
    return detail
