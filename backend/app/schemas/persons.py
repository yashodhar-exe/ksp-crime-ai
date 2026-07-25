from typing import Optional
from pydantic import BaseModel


class PersonCaseLinkOut(BaseModel):
    case_master_id: int
    crime_no: str
    crime_sub_head_name: Optional[str]
    case_status_name: Optional[str]
    role: str  # "Accused" | "Victim" | "Complainant"
    person_name: str
    age_year: Optional[int] = None


class PersonSearchResponse(BaseModel):
    query: str
    results: list[PersonCaseLinkOut]


class CoAccusedOut(BaseModel):
    accused_name: str
    shared_case_master_ids: list[int]
    case_count: int
