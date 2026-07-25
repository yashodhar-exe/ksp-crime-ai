from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    officer_id: Mapped[str | None] = mapped_column(String(10), nullable=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    role_id: Mapped[str] = mapped_column(String(10), ForeignKey("roles.role_id"), nullable=False)
    station_id: Mapped[str | None] = mapped_column(String(10), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Active")
    last_login: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Not part of schema.sql (auth needs a credential store) — see note in
    # core/security.py. Added here rather than a separate table to keep the
    # login flow a single query; nullable so existing seeded rows still load.
    hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)

    role: Mapped["Role"] = relationship(back_populates="users")  # noqa: F821
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="user")  # noqa: F821
