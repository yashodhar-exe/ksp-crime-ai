from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.core.rbac import scoped_district
from app.db.session import get_db
from app.models.digital_evidence import DigitalEvidence
from app.models.evidence import Evidence
from app.models.investigation_note import InvestigationNote
from app.models.suspect import Suspect
from app.models.timeline_event import TimelineEvent
from app.models.user import User
from app.models.victim import Victim
from app.schemas.case import (
    CaseCreate,
    CaseDetailOut,
    CaseListOut,
    CaseOut,
    CaseUpdate,
    DigitalEvidenceOut,
    EvidenceOut,
    InvestigationNoteOut,
    SimilarCaseOut,
    SuspectOut,
    TimelineEventOut,
    VictimOut,
)
from app.schemas.common import Page
from app.services import case_service, similarity_service
from app.services.audit_service import log_action

router = APIRouter(prefix="/cases", tags=["cases"])


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def _generate_case_id(db: Session) -> str:
    import uuid

    return f"CASE{uuid.uuid4().hex[:8].upper()}"


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
    user_district = current_user.station.district if current_user.station else None
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
    case_id: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CaseDetailOut:
    case = case_service.get_case(db, case_id)
    if case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")

    log_action(db, user_id=current_user.user_id, action="Viewed Case", case_id=case_id, ip_address=_client_ip(request))

    detail = CaseDetailOut.model_validate(case)
    detail.station_name = case.station.station_name if case.station else None
    detail.officer_name = case.officer.name if case.officer else None
    return detail


@router.post("", response_model=CaseOut, status_code=status.HTTP_201_CREATED)
def create_case(
    payload: CaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("can_edit_case")),
) -> CaseOut:
    case_id = _generate_case_id(db)
    case = case_service.create_case(db, case_id, payload.model_dump())
    return case


@router.patch("/{case_id}", response_model=CaseOut)
def update_case(
    case_id: str,
    payload: CaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("can_edit_case")),
) -> CaseOut:
    case = case_service.get_case(db, case_id)
    if case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
    return case_service.update_case(db, case, payload.model_dump(exclude_unset=True))


@router.get("/{case_id}/suspects", response_model=list[SuspectOut])
def get_case_suspects(case_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[SuspectOut]:
    _require_case(db, case_id)
    return db.query(Suspect).filter(Suspect.case_id == case_id).all()


@router.get("/{case_id}/victims", response_model=list[VictimOut])
def get_case_victims(case_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[VictimOut]:
    _require_case(db, case_id)
    return db.query(Victim).filter(Victim.case_id == case_id).all()


@router.get("/{case_id}/evidence", response_model=list[EvidenceOut])
def get_case_evidence(case_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[EvidenceOut]:
    _require_case(db, case_id)
    return db.query(Evidence).filter(Evidence.case_id == case_id).all()


@router.get("/{case_id}/digital-evidence", response_model=list[DigitalEvidenceOut])
def get_case_digital_evidence(
    case_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> list[DigitalEvidenceOut]:
    _require_case(db, case_id)
    return db.query(DigitalEvidence).filter(DigitalEvidence.case_id == case_id).all()


@router.get("/{case_id}/notes", response_model=list[InvestigationNoteOut])
def get_case_notes(case_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[InvestigationNoteOut]:
    _require_case(db, case_id)
    return db.query(InvestigationNote).filter(InvestigationNote.case_id == case_id).all()


@router.get("/{case_id}/timeline", response_model=list[TimelineEventOut])
def get_case_timeline(case_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[TimelineEventOut]:
    _require_case(db, case_id)
    return db.query(TimelineEvent).filter(TimelineEvent.case_id == case_id).order_by(TimelineEvent.event_id).all()


@router.get("/{case_id}/similar-cases", response_model=list[SimilarCaseOut])
def get_similar_cases(
    case_id: str,
    limit: int = Query(default=10, le=50),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[SimilarCaseOut]:
    case = _require_case(db, case_id)
    pairs = similarity_service.find_similar_cases(db, case, limit=limit)
    return [
        SimilarCaseOut(
            case_id=c.case_id,
            fir_number=c.fir_number,
            crime_type=c.crime_type,
            status=c.status,
            district=c.district,
            pattern_id=c.pattern_id,
            similarity_reason=reason,
        )
        for c, reason in pairs
    ]


def _require_case(db: Session, case_id: str):
    case = case_service.get_case(db, case_id)
    if case is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")
    return case
