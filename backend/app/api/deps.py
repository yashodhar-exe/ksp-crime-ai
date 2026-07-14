from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.rbac import has_permission
from app.core.security import JWTError, decode_token
from app.db.session import get_db
from app.models.user import User

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(reusable_oauth2),
    db: Session = Depends(get_db),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
    except JWTError as exc:
        raise credentials_error from exc

    if payload.get("type") != "access":
        raise credentials_error

    user_id = payload.get("sub")
    user = db.get(User, user_id) if user_id else None
    if user is None:
        raise credentials_error
    if user.status != "Active":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is not active")
    return user


def require_role(permission: str) -> Callable[[User], User]:
    """
    Usage: `current_user: User = Depends(require_role("can_manage_users"))`
    Checks the boolean permission columns on the user's role (see
    core/rbac.py + roles table in schema.sql).
    """

    def _checker(current_user: User = Depends(get_current_user)) -> User:
        if not has_permission(current_user.role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permission: {permission}",
            )
        return current_user

    return _checker
