from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id: Mapped[str] = mapped_column(String(12), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(10), ForeignKey("users.user_id"), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    case_id: Mapped[str | None] = mapped_column(String(12), ForeignKey("cases.case_id"), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)

    user: Mapped["User"] = relationship(back_populates="audit_logs")  # noqa: F821
    case: Mapped["Case | None"] = relationship()  # noqa: F821
