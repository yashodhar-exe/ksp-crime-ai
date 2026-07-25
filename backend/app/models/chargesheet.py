from __future__ import annotations
from typing import Optional

from datetime import datetime

from sqlalchemy import CHAR, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ChargesheetDetails(Base):
    """Final report on a case: A = Chargesheet, B = False Case, C = Undetected."""

    __tablename__ = "chargesheet_details"

    csid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_master_id: Mapped[int] = mapped_column(Integer, ForeignKey("case_master.case_master_id"), nullable=False)
    csdate: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    cstype: Mapped[str] = mapped_column(CHAR(1), nullable=False)  # A / B / C
    police_person_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("employee.employee_id"), nullable=True)

    case: Mapped["CaseMaster"] = relationship(back_populates="chargesheets")  # noqa: F821
    police_person: Mapped["Employee"] = relationship(back_populates="chargesheets")  # noqa: F821
