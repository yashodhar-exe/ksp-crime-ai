from typing import Optional
from app.schemas.common import ORMModel


class CitizenOut(ORMModel):
    citizen_id: str
    first_name: str
    last_name: str
    gender: str
    age: int
    phone: str
    email: Optional[str]
    address: Optional[str]
    city: str
    district: str


class CitizenCaseLinkOut(ORMModel):
    case_id: str
    fir_number: str
    crime_type: str
    status: str
    role: str  # "Suspect" | "Victim"


class RelationshipOut(ORMModel):
    relationship_id: str
    citizen_1: str
    citizen_2: str
    relationship_type: str


class PhoneOut(ORMModel):
    phone_id: str
    phone_number: str
    provider: Optional[str]


class VehicleOut(ORMModel):
    vehicle_id: str
    vehicle_number: str
    vehicle_type: Optional[str]


class BankAccountOut(ORMModel):
    account_id: str
    bank_name: str
    account_number: str
    ifsc: Optional[str]


class CitizenAssetsOut(ORMModel):
    phones: list[PhoneOut]
    vehicles: list[VehicleOut]
    bank_accounts: list[BankAccountOut]
