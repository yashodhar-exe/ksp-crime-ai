from typing import Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.core.security import hash_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.audit import UserCreate, UserOut, UserUpdate
from app.services.audit_service import log_action

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserOut])
def list_users(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by exact status, e.g. 'Pending', 'Active'"),
    db: Session = Depends(get_db),
    _: User = Depends(require_role("can_manage_users")),
) -> list[UserOut]:
    stmt = select(User).order_by(User.username)
    if status_filter:
        stmt = stmt.where(User.status == status_filter)
    return db.execute(stmt).scalars().all()


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("can_manage_users")),
) -> UserOut:
    existing = db.execute(select(User).where(User.username == payload.username)).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    user = User(
        user_id=f"USR{uuid.uuid4().hex[:7].upper()}",
        username=payload.username,
        hashed_password=hash_password(payload.password),
        role_id=payload.role_id,
        officer_id=payload.officer_id,
        station_id=payload.station_id,
        status="Active",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.patch("/{user_id}", response_model=UserOut)
def update_user(
    user_id: str,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("can_manage_users")),
) -> UserOut:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    data = payload.model_dump(exclude_unset=True)
    if "password" in data:
        password = data.pop("password")
        if password:
            user.hashed_password = hash_password(password)
    for field, value in data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


@router.post("/{user_id}/approve", response_model=UserOut)
def approve_user(
    user_id: str,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("can_manage_users")),
) -> UserOut:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.status != "Pending":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only pending accounts can be approved")

    user.status = "Active"
    db.commit()
    db.refresh(user)

    log_action(
        db,
        user_id=admin.user_id,
        action=f"Approved User: {user.username}"[:50],
        ip_address=request.client.host if request.client else "unknown",
    )
    return user


@router.post("/{user_id}/reject", response_model=UserOut)
def reject_user(
    user_id: str,
    request: Request,
    db: Session = Depends(get_db),
    admin: User = Depends(require_role("can_manage_users")),
) -> UserOut:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.status != "Pending":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only pending accounts can be rejected")

    user.status = "Rejected"
    db.commit()
    db.refresh(user)

    log_action(
        db,
        user_id=admin.user_id,
        action=f"Rejected User: {user.username}"[:50],
        ip_address=request.client.host if request.client else "unknown",
    )
    return user
