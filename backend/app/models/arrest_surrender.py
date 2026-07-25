from __future__ import annotations
from typing import Optional

from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ArrestSurrender(Base):
    __tablename__ = "arrest_surrender"

    arrest_surrender_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_master_id: Mapped[int] = mapped_column(Integer, ForeignKey("case_master.case_master_id"), nullable=False)
    arrest_surrender_type_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # lookup: arrest / surrender
    arrest_surrender_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    arrest_surrender_state_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("state.state_id"), nullable=True)
    arrest_surrender_district_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("district.district_id"), nullable=True
    )
    police_station_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("unit.unit_id"), nullable=True)
    io_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("employee.employee_id"), nullable=True)
    court_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("court.court_id"), nullable=True)
    accused_master_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("accused.accused_master_id"), nullable=True)
    is_accused: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_complainant_accused: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    case: Mapped["CaseMaster"] = relationship(back_populates="arrest_surrenders")  # noqa: F821
    state: Mapped["State"] = relationship()  # noqa: F821
    district: Mapped["District"] = relationship()  # noqa: F821
    police_station: Mapped["Unit"] = relationship()  # noqa: F821
    investigating_officer: Mapped["Employee"] = relationship(back_populates="investigated_arrests")  # noqa: F821
    court: Mapped["Court"] = relationship()  # noqa: F821
    accused: Mapped["Optional[Accused]"] = relationship(back_populates="arrest_surrenders")  # noqa: F821

    accused_links: Mapped[list["InvArrestSurrenderAccused"]] = relationship(
        back_populates="arrest_surrender", cascade="all, delete-orphan"
    )


class InvArrestSurrenderAccused(Base):
    """Junction table: one arrest/surrender event can (in general) cover multiple accused."""

    __tablename__ = "inv_arrestsurrenderaccused"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    arrest_surrender_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("arrest_surrender.arrest_surrender_id"), nullable=False
    )
    accused_master_id: Mapped[int] = mapped_column(Integer, ForeignKey("accused.accused_master_id"), nullable=False)

    arrest_surrender: Mapped["ArrestSurrender"] = relationship(back_populates="accused_links")
    accused: Mapped["Accused"] = relationship(back_populates="arrest_links")
