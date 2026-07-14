from datetime import date

from pydantic import BaseModel

from app.schemas.common import ORMModel, Page


class CaseOut(ORMModel):
    case_id: str
    fir_number: str
    crime_type: str
    station_id: str
    officer_id: str
    status: str
    priority: str
    incident_date: date
    registered_date: date
    city: str
    district: str
    estimated_loss: int
    pattern_id: str | None


class CaseDetailOut(CaseOut):
    description: str | None
    complaint_text: str
    station_name: str | None = None
    officer_name: str | None = None


class CaseListOut(BaseModel):
    items: list[CaseOut]
    page: Page


class CaseCreate(BaseModel):
    fir_number: str
    crime_type: str
    station_id: str
    officer_id: str
    status: str = "Open"
    priority: str = "Medium"
    incident_date: date
    registered_date: date
    city: str
    district: str
    description: str | None = None
    estimated_loss: int = 0
    complaint_text: str
    pattern_id: str | None = None


class CaseUpdate(BaseModel):
    status: str | None = None
    priority: str | None = None
    description: str | None = None
    pattern_id: str | None = None


class SuspectOut(ORMModel):
    suspect_id: str
    case_id: str
    citizen_id: str
    role: str
    arrest_status: str


class VictimOut(ORMModel):
    victim_id: str
    case_id: str
    citizen_id: str
    injury_level: str


class EvidenceOut(ORMModel):
    evidence_id: str
    case_id: str
    evidence_type: str
    description: str | None
    status: str
    collected_by: str | None


class DigitalEvidenceOut(ORMModel):
    digital_evidence_id: str
    case_id: str
    file_type: str
    file_name: str | None
    phone_number: str | None
    email: str | None
    ip_address: str | None
    uploaded_by: str | None
    status: str
    extracted_entities: str | None


class InvestigationNoteOut(ORMModel):
    note_id: str
    case_id: str
    officer_id: str
    note: str


class TimelineEventOut(ORMModel):
    event_id: str
    case_id: str
    event: str


class SimilarCaseOut(ORMModel):
    case_id: str
    fir_number: str
    crime_type: str
    status: str
    district: str
    pattern_id: str | None
    similarity_reason: str
