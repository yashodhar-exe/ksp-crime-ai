from typing import Optional
from pydantic import BaseModel


class CrimeTrendPoint(BaseModel):
    period: str
    crime_group_name: str
    count: int


class CrimeTrendsOut(BaseModel):
    district: Optional[str]
    period: str
    points: list[CrimeTrendPoint]


class HotspotOut(BaseModel):
    district_name: str
    case_count: int
    top_crime_group_name: Optional[str] = None


class CrimeHeadOut(BaseModel):
    crime_head_id: int
    crime_group_name: str
    case_count: int
