from pydantic import BaseModel

from app.schemas.common import ORMModel


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class RegisterRequest(BaseModel):
    username: str
    password: str
    role_id: str


class RegisterResponse(BaseModel):
    user_id: str
    username: str
    status: str
    message: str


class CurrentUserOut(ORMModel):
    user_id: str
    username: str
    role_id: str
    officer_id: str | None
    station_id: str | None
    status: str
