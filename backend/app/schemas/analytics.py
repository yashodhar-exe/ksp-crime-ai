from pydantic import BaseModel


class CrimeTrendPoint(BaseModel):
    period: str
    crime_group_name: str
    count: int


class CrimeTrendsOut(BaseModel):
    district: str | None
    period: str
    points: list[CrimeTrendPoint]


class HotspotOut(BaseModel):
    district_name: str
    case_count: int
    top_crime_group_name: str | None = None


class CrimeHeadOut(BaseModel):
    crime_head_id: int
    crime_group_name: str
    case_count: int
