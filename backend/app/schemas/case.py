from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel, Page


class ComplainantOut(ORMModel):
    complainant_id: int
    case_master_id: int
    complainant_name: str
    age_year: int | None = None
    occupation_id: int | None = None
    religion_id: int | None = None
    caste_id: int | None = None
    gender_id: int | None = None


class ActSectionOut(ORMModel):
    id: int
    case_master_id: int
    act_id: str
    section_id: str
    act_order_id: int | None = None
    section_order_id: int | None = None


class VictimOut(ORMModel):
    victim_master_id: int
    case_master_id: int
    victim_name: str
    age_year: int | None = None
    gender_id: str | None = None
    victim_police: bool = False


class AccusedOut(ORMModel):
    accused_master_id: int
    case_master_id: int
    accused_name: str
    age_year: int | None = None
    gender_id: str | None = None
    person_id: str | None = None


class ArrestSurrenderOut(ORMModel):
    arrest_surrender_id: int
    case_master_id: int
    arrest_surrender_type_id: int | None = None
    arrest_surrender_date: date | None = None
    arrest_surrender_state_id: int | None = None
    arrest_surrender_district_id: int | None = None
    police_station_id: int | None = None
    io_id: int | None = None
    court_id: int | None = None
    accused_master_id: int | None = None
    is_accused: bool = False
    is_complainant_accused: bool = False


class ChargesheetOut(ORMModel):
    csid: int
    case_master_id: int
    csdate: datetime | None = None
    cstype: str
    police_person_id: int | None = None


class CaseOut(ORMModel):
    case_master_id: int
    crime_no: str
    case_no: str
    crime_registered_date: date
    police_person_id: int
    police_station_id: int
    case_category_id: int
    gravity_offence_id: int | None = None
    crime_major_head_id: int | None = None
    crime_minor_head_id: int | None = None
    case_status_id: int
    court_id: int | None = None
    incident_from_date: datetime | None = None
    incident_to_date: datetime | None = None
    latitude: float | None = None
    longitude: float | None = None

    case_category_name: str | None = None
    case_status_name: str | None = None
    gravity_name: str | None = None
    crime_head_name: str | None = None
    crime_sub_head_name: str | None = None
    police_station_name: str | None = None
    district_name: str | None = None


class CaseDetailOut(CaseOut):
    info_received_ps_date: datetime | None = None
    brief_facts: str | None = None
    registering_officer_name: str | None = None
    court_name: str | None = None

    complainants: list[ComplainantOut] = Field(default_factory=list)
    act_sections: list[ActSectionOut] = Field(default_factory=list)
    victims: list[VictimOut] = Field(default_factory=list)
    accused: list[AccusedOut] = Field(default_factory=list)
    arrest_surrenders: list[ArrestSurrenderOut] = Field(default_factory=list)
    chargesheets: list[ChargesheetOut] = Field(default_factory=list)


class CaseListOut(BaseModel):
    items: list[CaseOut]
    page: Page


class SimilarCaseOut(BaseModel):
    case_master_id: int
    crime_no: str
    crime_sub_head_name: str | None = None
    case_status_name: str | None = None
    district_name: str | None = None
    similarity_reason: str
