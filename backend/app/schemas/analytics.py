from pydantic import BaseModel


class CrimeTrendPoint(BaseModel):
    period: str
    crime_type: str
    count: int


class CrimeTrendsOut(BaseModel):
    district: str | None
    period: str
    points: list[CrimeTrendPoint]


class HotspotOut(BaseModel):
    district: str
    case_count: int
    top_crime_type: str | None = None


class PatternSummaryOut(BaseModel):
    pattern_id: str
    crime_type: str
    modus_operandi: str | None
    risk_level: str
    case_count: int
