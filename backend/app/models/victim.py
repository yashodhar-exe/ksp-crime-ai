from typing import Optional
from sqlalchemy import ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Victim(Base):
    __tablename__ = "victim"

    victim_master_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    case_master_id: Mapped[int] = mapped_column(Integer, ForeignKey("case_master.case_master_id"), nullable=False)
    victim_name: Mapped[str] = mapped_column(String(150), nullable=False)
    age_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    gender_id: Mapped[Optional[str]] = mapped_column(String(1), nullable=True)
    victim_police: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    case: Mapped["CaseMaster"] = relationship(back_populates="victims")  # noqa: F821
