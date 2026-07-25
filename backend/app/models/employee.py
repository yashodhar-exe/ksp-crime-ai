from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Employee(Base):
    """Police personnel. Referenced by CaseMaster.PolicePersonID, ArrestSurrender.IOID, etc."""

    __tablename__ = "employee"

    employee_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    district_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("district.district_id"), nullable=True)
    unit_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("unit.unit_id"), nullable=True)
    rank_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("rank_master.rank_id"), nullable=True)
    designation_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("designation.designation_id"), nullable=True
    )
    kgid: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    employee_dob: Mapped[date | None] = mapped_column(Date, nullable=True)
    gender_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    blood_group_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    physically_challenged: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    appointment_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    district: Mapped["District"] = relationship(back_populates="employees")  # noqa: F821
    unit: Mapped["Unit"] = relationship(back_populates="employees")  # noqa: F821
    rank: Mapped["Rank"] = relationship(back_populates="employees")  # noqa: F821
    designation: Mapped["Designation"] = relationship(back_populates="employees")  # noqa: F821

    registered_cases: Mapped[list["CaseMaster"]] = relationship(  # noqa: F821
        back_populates="registering_officer", foreign_keys="CaseMaster.police_person_id"
    )
    investigated_arrests: Mapped[list["ArrestSurrender"]] = relationship(back_populates="investigating_officer")  # noqa: F821
    chargesheets: Mapped[list["ChargesheetDetails"]] = relationship(back_populates="police_person")  # noqa: F821
