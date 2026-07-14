from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Role(Base):
    __tablename__ = "roles"

    role_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    role_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    can_view_all_districts: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_export: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_edit_case: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_manage_users: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    users: Mapped[list["User"]] = relationship(back_populates="role")  # noqa: F821
