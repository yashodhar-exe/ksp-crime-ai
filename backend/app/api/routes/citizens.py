from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.bank_account import BankAccount
from app.models.citizen import Citizen
from app.models.criminal_relationship import CriminalRelationship
from app.models.phone import Phone
from app.models.suspect import Suspect
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.victim import Victim
from app.schemas.citizen import (
    BankAccountOut,
    CitizenAssetsOut,
    CitizenCaseLinkOut,
    CitizenOut,
    PhoneOut,
    RelationshipOut,
    VehicleOut,
)

router = APIRouter(prefix="/citizens", tags=["citizens"])


def _require_citizen(db: Session, citizen_id: str) -> Citizen:
    citizen = db.get(Citizen, citizen_id)
    if citizen is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Citizen not found")
    return citizen


@router.get("/{citizen_id}", response_model=CitizenOut)
def get_citizen(citizen_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> CitizenOut:
    return _require_citizen(db, citizen_id)


@router.get("/{citizen_id}/cases", response_model=list[CitizenCaseLinkOut])
def get_citizen_cases(citizen_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> list[CitizenCaseLinkOut]:
    _require_citizen(db, citizen_id)

    links: list[CitizenCaseLinkOut] = []

    suspect_stmt = select(Suspect).where(Suspect.citizen_id == citizen_id)
    for s in db.execute(suspect_stmt).scalars().all():
        links.append(
            CitizenCaseLinkOut(
                case_id=s.case.case_id,
                fir_number=s.case.fir_number,
                crime_type=s.case.crime_type,
                status=s.case.status,
                role="Suspect",
            )
        )

    victim_stmt = select(Victim).where(Victim.citizen_id == citizen_id)
    for v in db.execute(victim_stmt).scalars().all():
        links.append(
            CitizenCaseLinkOut(
                case_id=v.case.case_id,
                fir_number=v.case.fir_number,
                crime_type=v.case.crime_type,
                status=v.case.status,
                role="Victim",
            )
        )

    return links


@router.get("/{citizen_id}/relationships", response_model=list[RelationshipOut])
def get_citizen_relationships(
    citizen_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)
) -> list[RelationshipOut]:
    _require_citizen(db, citizen_id)
    stmt = select(CriminalRelationship).where(
        or_(CriminalRelationship.citizen_1 == citizen_id, CriminalRelationship.citizen_2 == citizen_id)
    )
    return db.execute(stmt).scalars().all()


@router.get("/{citizen_id}/assets", response_model=CitizenAssetsOut)
def get_citizen_assets(citizen_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)) -> CitizenAssetsOut:
    _require_citizen(db, citizen_id)

    phones = db.execute(select(Phone).where(Phone.citizen_id == citizen_id)).scalars().all()
    vehicles = db.execute(select(Vehicle).where(Vehicle.citizen_id == citizen_id)).scalars().all()
    accounts = db.execute(select(BankAccount).where(BankAccount.citizen_id == citizen_id)).scalars().all()

    return CitizenAssetsOut(
        phones=[PhoneOut.model_validate(p) for p in phones],
        vehicles=[VehicleOut.model_validate(v) for v in vehicles],
        bank_accounts=[BankAccountOut.model_validate(a) for a in accounts],
    )
