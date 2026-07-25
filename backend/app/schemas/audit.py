from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel


class AuditLogOut(ORMModel):
    log_id: str
    user_id: str
    action: str
    case_id: Optional[str]
    timestamp: datetime
    ip_address: str


class UserOut(ORMModel):
    user_id: str
    officer_id: Optional[str]
    username: str
    role_id: str
    station_id: Optional[str]
    status: str
    last_login: Optional[datetime]


class UserCreate(BaseModel):
    username: str
    password: str
    role_id: str
    officer_id: Optional[str] = None
    station_id: Optional[str] = None


class UserUpdate(BaseModel):
    role_id: Optional[str] = None
    station_id: Optional[str] = None
    status: Optional[str] = None
    password: Optional[str] = None
