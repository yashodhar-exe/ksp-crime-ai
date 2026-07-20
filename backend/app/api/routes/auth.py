import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import (
    JWTError,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.db.session import get_db
from app.models.role import Role
from app.models.user import User
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, RegisterResponse, TokenResponse
from app.services.audit_service import log_action

router = APIRouter(prefix="/auth", tags=["auth"])

# Admin accounts are never self-service — only an existing admin can create
# one (via POST /users). Every other role can be requested at signup, but
# the account sits as "Pending" until an admin approves it (see
# api/routes/users.py: approve_user / reject_user).
NON_SELF_REGISTRABLE_ROLES = {"ROLE01"}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)) -> TokenResponse:
    stmt = select(User).where(User.username == payload.username)
    user = db.execute(stmt).scalar_one_or_none()

    if user is None or not user.hashed_password or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    if user.status == "Pending":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is pending admin approval. You'll be able to log in once an administrator approves it.",
        )
    if user.status == "Rejected":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your registration was not approved. Contact an administrator for details.",
        )
    if user.status != "Active":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is not active")

    access_token = create_access_token(user.user_id, user.role_id, user.station_id)
    refresh_token = create_refresh_token(user.user_id)

    log_action(
        db,
        user_id=user.user_id,
        action="Logged In",
        ip_address=request.client.host if request.client else "unknown",
    )

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, request: Request, db: Session = Depends(get_db)) -> RegisterResponse:
    """
    Public self-registration. The account is created with status='Pending'
    and cannot log in (see `login` above) until an admin approves it via
    POST /users/{user_id}/approve.
    """
    if payload.role_id in NON_SELF_REGISTRABLE_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This role cannot be self-registered. Contact an administrator.",
        )

    role = db.get(Role, payload.role_id)
    if role is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid role selected.")

    if len(payload.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must be at least 8 characters.",
        )

    existing = db.execute(select(User).where(User.username == payload.username)).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    user = User(
        user_id=f"USR{uuid.uuid4().hex[:7].upper()}",
        username=payload.username,
        hashed_password=hash_password(payload.password),
        role_id=payload.role_id,
        status="Pending",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    log_action(
        db,
        user_id=user.user_id,
        action="Self-Registered (Pending)",
        ip_address=request.client.host if request.client else "unknown",
    )

    return RegisterResponse(
        user_id=user.user_id,
        username=user.username,
        status=user.status,
        message="Registration submitted. An administrator must approve your account before you can log in.",
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)) -> TokenResponse:
    try:
        claims = decode_token(payload.refresh_token)
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from exc

    if claims.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    user = db.get(User, claims.get("sub"))
    if user is None or user.status != "Active":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = create_access_token(user.user_id, user.role_id, user.station_id)
    new_refresh_token = create_refresh_token(user.user_id)
    return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    # Stateless JWTs: nothing to invalidate server-side without a token
    # blocklist. Logged for the audit trail; the client is responsible for
    # discarding the tokens.
    log_action(
        db,
        user_id=current_user.user_id,
        action="Logged Out",
        ip_address=request.client.host if request.client else "unknown",
    )
    return None
