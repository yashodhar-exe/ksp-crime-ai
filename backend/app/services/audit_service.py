from typing import Optional
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def _utcnow_naive() -> datetime:
    """schema.sql defines audit_logs.timestamp as TIMESTAMP (no tz)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _new_log_id() -> str:
    return f"LOG{uuid.uuid4().hex[:9].upper()}"


def log_action(
    db: Session,
    *,
    user_id: str,
    action: str,
    ip_address: str,
    case_id: Optional[str] = None,
    commit: bool = True,
) -> AuditLog:
    """
    Recorded actions per schema.sql: 'Viewed Case', 'Downloaded Report',
    'Updated Evidence', 'Searched Entity', 'Viewed Suspect Profile'.
    Called from route handlers (thin) rather than buried in middleware, so
    each router stays explicit about what it logs and why.
    """
    entry = AuditLog(
        log_id=_new_log_id(),
        user_id=user_id,
        action=action,
        case_id=case_id,
        timestamp=_utcnow_naive(),
        ip_address=ip_address,
    )
    db.add(entry)
    if commit:
        db.commit()
        db.refresh(entry)
    return entry
