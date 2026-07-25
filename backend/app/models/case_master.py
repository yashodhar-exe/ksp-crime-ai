from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CaseMaster(Base):
    """The FIR / UDR / PAR / Zero-FIR record. One row per registered case."""

    __tablename__ = "case_master"

    case_master_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # CrimeNo = 1-digit category + 4-digit district + 4-digit station(unit) + 4-digit year + 5-digit serial
    crime_no: Mapped[str] = mapped_column(String(18), nullable=False, unique=True)
    # CaseNo = last 9 digits of CrimeNo: YYYY + 5-digit running serial
    case_no: Mapped[str] = mapped_column(String(9), nullable=False)

    crime_registered_date: Mapped[date] = mapped_column(Date, nullable=False)

    police_person_id: Mapped[int] = mapped_column(Integer, ForeignKey("employee.employee_id"), nullable=False)
    police_station_id: Mapped[int] = mapped_column(Integer, ForeignKey("unit.unit_id"), nullable=False)
    case_category_id: Mapped[int] = mapped_column(Integer, ForeignKey("case_category.case_category_id"), nullable=False)
    gravity_offence_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("gravity_offence.gravity_offence_id"), nullable=True
    )
    crime_major_head_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("crime_head.crime_head_id"), nullable=True
    )
    crime_minor_head_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("crime_sub_head.crime_sub_head_id"), nullable=True
    )
    case_status_id: Mapped[int] = mapped_column(Integer, ForeignKey("case_status_master.case_status_id"), nullable=False)
    court_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("court.court_id"), nullable=True)

    incident_from_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    incident_to_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    info_received_ps_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    latitude: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    longitude: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)

    brief_facts: Mapped[str | None] = mapped_column(Text, nullable=True)

    # --- relationships ---
    registering_officer: Mapped["Employee"] = relationship(  # noqa: F821
        back_populates="registered_cases", foreign_keys=[police_person_id]
    )
    police_station: Mapped["Unit"] = relationship(back_populates="cases")  # noqa: F821
    case_category: Mapped["CaseCategory"] = relationship(back_populates="cases")  # noqa: F821
    gravity_offence: Mapped["GravityOffence"] = relationship(back_populates="cases")  # noqa: F821
    crime_major_head: Mapped["CrimeHead"] = relationship(back_populates="cases")  # noqa: F821
    crime_minor_head: Mapped["CrimeSubHead"] = relationship(back_populates="cases")  # noqa: F821
    case_status: Mapped["CaseStatusMaster"] = relationship(back_populates="cases")  # noqa: F821
    court: Mapped["Court | None"] = relationship(back_populates="cases")  # noqa: F821

    complainants: Mapped[list["ComplainantDetails"]] = relationship(  # noqa: F821
        back_populates="case", cascade="all, delete-orphan"
    )
    act_sections: Mapped[list["ActSectionAssociation"]] = relationship(  # noqa: F821
        back_populates="case", cascade="all, delete-orphan"
    )
    victims: Mapped[list["Victim"]] = relationship(back_populates="case", cascade="all, delete-orphan")  # noqa: F821
    accused: Mapped[list["Accused"]] = relationship(back_populates="case", cascade="all, delete-orphan")  # noqa: F821
    arrest_surrenders: Mapped[list["ArrestSurrender"]] = relationship(  # noqa: F821
        back_populates="case", cascade="all, delete-orphan"
    )
    chargesheets: Mapped[list["ChargesheetDetails"]] = relationship(  # noqa: F821
        back_populates="case", cascade="all, delete-orphan"
    )
