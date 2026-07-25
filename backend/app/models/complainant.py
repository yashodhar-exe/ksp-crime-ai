from __future__ import annotations
from typing import Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ComplainantDetails(Base):
    __tablename__ = "complainant_details"

    complainant_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_master_id: Mapped[int] = mapped_column(Integer, ForeignKey("case_master.case_master_id"), nullable=False)
    complainant_name: Mapped[str] = mapped_column(String(150), nullable=False)
    age_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    occupation_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("occupation_master.occupation_id"), nullable=True)
    religion_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("religion_master.religion_id"), nullable=True)
    caste_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("caste_master.caste_master_id"), nullable=True)
    gender_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    case: Mapped["CaseMaster"] = relationship(back_populates="complainants")  # noqa: F821
    occupation: Mapped["OccupationMaster"] = relationship(back_populates="complainants")  # noqa: F821
    religion: Mapped["ReligionMaster"] = relationship(back_populates="complainants")  # noqa: F821
    caste: Mapped["CasteMaster"] = relationship(back_populates="complainants")  # noqa: F821
