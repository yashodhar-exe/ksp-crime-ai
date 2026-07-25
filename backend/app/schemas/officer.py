from typing import Optional
from app.schemas.common import ORMModel


class OfficerOut(ORMModel):
    officer_id: str
    name: str
    rank: str
    station_id: str
    phone: str
    email: Optional[str]


class StationOut(ORMModel):
    station_id: str
    station_name: str
    district: str
    city: str
    phone: str
