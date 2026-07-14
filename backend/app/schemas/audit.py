from datetime import date, datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel


class AuditLogOut(ORMModel):
    log_id: str
    user_id: str
    action: str
    case_id: str | None
    timestamp: datetime
    ip_address: str


class UserOut(ORMModel):
    user_id: str
    officer_id: str | None
    username: str
    role_id: str
    station_id: str | None
    status: str
    last_login: date | None


class UserCreate(BaseModel):
    username: str
    password: str
    role_id: str
    officer_id: str | None = None
    station_id: str | None = None


class UserUpdate(BaseModel):
    role_id: str | None = None
    station_id: str | None = None
    status: str | None = None
    password: str | None = None
