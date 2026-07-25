from pydantic import BaseModel


class PersonCaseLinkOut(BaseModel):
    case_master_id: int
    crime_no: str
    crime_sub_head_name: str | None
    case_status_name: str | None
    role: str  # "Accused" | "Victim" | "Complainant"
    person_name: str
    age_year: int | None = None


class PersonSearchResponse(BaseModel):
    query: str
    results: list[PersonCaseLinkOut]


class CoAccusedOut(BaseModel):
    accused_name: str
    shared_case_master_ids: list[int]
    case_count: int
