from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.core.rbac import scoped_district
from app.db.session import get_db
from app.models.user import User
from app.schemas.case import (
    CaseDetailOut,
    CaseListOut,
    CaseOut,
    SimilarCaseOut,
)
from app.schemas.common import Page
from app.services import case_service, similarity_service
from app.services.audit_service import log_action

router = APIRouter(prefix="/cases", tags=["cases"])


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


@router.get("", response_model=CaseListOut)
def list_cases(
    crime_type: str | None = None,
    status_: str | None = Query(default=None, alias="status"),
    district: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CaseListOut:
    # TODO: Fetch district from station_id if needed, but for now fallback to None
    user_district = None
    district_filter = scoped_district(current_user.role, user_district)

    items, total = case_service.list_cases(
        db,
        crime_type=crime_type,
        status=status_,
        district=district,
        date_from=date_from,
        date_to=date_to,
        scoped_district=district_filter,
        limit=limit,
        offset=offset,
    )
    return CaseListOut(items=items, page=Page(total=total, limit=limit, offset=offset))


@router.get("/{case_id}", response_model=CaseDetailOut)
def get_case(
    case_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CaseDetailOut:
    case = case_service.get_case(db, case_id)
    if case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")

    log_action(db, user_id=current_user.user_id, action="Viewed Case", ip_address=_client_ip(request))
    return CaseDetailOut.model_validate(case)


@router.get("/{case_id}/similar-cases", response_model=list[SimilarCaseOut])
def get_similar_cases(
    case_id: int,
    limit: int = Query(default=10, le=50),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[SimilarCaseOut]:
    case = case_service.get_case(db, case_id)
    if case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
    
    pairs = similarity_service.find_similar_cases(db, case, limit=limit)
    return [
        SimilarCaseOut(
            case_master_id=c.case_master_id,
            crime_no=c.crime_no,
            crime_sub_head_name=c.crime_sub_head_name,
            case_status_name=c.case_status_name,
            district_name=c.district_name,
            similarity_reason=reason,
        )
        for c, reason in pairs
    ]
