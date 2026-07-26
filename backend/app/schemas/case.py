from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import ORMModel, Page


class ComplainantOut(ORMModel):
    complainant_id: int
    case_master_id: int
    complainant_name: str
    age_year: Optional[int] = None
    occupation_id: Optional[int] = None
    religion_id: Optional[int] = None
    caste_id: Optional[int] = None
    gender_id: Optional[int] = None


class ActSectionOut(ORMModel):
    id: int
    case_master_id: int
    act_id: str
    section_id: str
    act_order_id: Optional[int] = None
    section_order_id: Optional[int] = None


class VictimOut(ORMModel):
    victim_master_id: int
    case_master_id: int
    victim_name: str
    age_year: Optional[int] = None
    gender_id: Optional[str] = None
    victim_police: bool = False


class AccusedOut(ORMModel):
    accused_master_id: int
    case_master_id: int
    accused_name: str
    age_year: Optional[int] = None
    gender_id: Optional[str] = None
    person_id: Optional[str] = None


class ArrestSurrenderOut(ORMModel):
    arrest_surrender_id: int
    case_master_id: int
    arrest_surrender_type_id: Optional[int] = None
    arrest_surrender_date: Optional[date] = None
    arrest_surrender_state_id: Optional[int] = None
    arrest_surrender_district_id: Optional[int] = None
    police_station_id: Optional[int] = None
    io_id: Optional[int] = None
    court_id: Optional[int] = None
    accused_master_id: Optional[int] = None
    is_accused: bool = False
    is_complainant_accused: bool = False


class ChargesheetOut(ORMModel):
    csid: int
    case_master_id: int
    csdate: Optional[datetime] = None
    cstype: str
    police_person_id: Optional[int] = None


class CaseOut(ORMModel):
    case_master_id: int
    crime_no: str
    case_no: str
    
    @field_validator('crime_no', 'case_no', mode='before')
    @classmethod
    def coerce_to_str(cls, v):
        return str(v) if v is not None else v
    crime_registered_date: date
    police_person_id: int
    police_station_id: int
    case_category_id: int
    gravity_offence_id: Optional[int] = None
    crime_major_head_id: Optional[int] = None
    crime_minor_head_id: Optional[int] = None
    case_status_id: int
    court_id: Optional[int] = None
    incident_from_date: Optional[datetime] = None
    incident_to_date: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    case_category_name: Optional[str] = None
    case_status_name: Optional[str] = None
    gravity_name: Optional[str] = None
    crime_head_name: Optional[str] = None
    crime_sub_head_name: Optional[str] = None
    police_station_name: Optional[str] = None
    district_name: Optional[str] = None


class CaseDetailOut(CaseOut):
    info_received_ps_date: Optional[datetime] = None
    brief_facts: Optional[str] = None
    registering_officer_name: Optional[str] = None
    court_name: Optional[str] = None

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
    
    @field_validator('crime_no', mode='before')
    @classmethod
    def coerce_to_str(cls, v):
        return str(v) if v is not None else v
    crime_sub_head_name: Optional[str] = None
    case_status_name: Optional[str] = None
    district_name: Optional[str] = None
    similarity_reason: str
