from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Accused(Base):
    __tablename__ = "accused"

    accused_master_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_master_id: Mapped[int] = mapped_column(Integer, ForeignKey("case_master.case_master_id"), nullable=False)
    accused_name: Mapped[str] = mapped_column(String(150), nullable=False)
    age_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    gender_id: Mapped[str | None] = mapped_column(String(1), nullable=True)  # M / F / T
    person_id: Mapped[str | None] = mapped_column(String(10), nullable=True)  # A1, A2, A3...

    case: Mapped["CaseMaster"] = relationship(back_populates="accused")  # noqa: F821
    arrest_surrenders: Mapped[list["ArrestSurrender"]] = relationship(back_populates="accused")  # noqa: F821
    arrest_links: Mapped[list["InvArrestSurrenderAccused"]] = relationship(back_populates="accused")  # noqa: F821
