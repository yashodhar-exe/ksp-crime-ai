from __future__ import annotations
from typing import Optional
"""
Master / lookup tables from the KSP Police FIR ER Diagram.
These are the low-churn reference tables that everything else hangs off of.
"""

from sqlalchemy import Boolean, ForeignKey, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class State(Base):
    __tablename__ = "state"

    state_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    state_name: Mapped[str] = mapped_column(String(100), nullable=False)
    nationality_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    districts: Mapped[list["District"]] = relationship(back_populates="state")
    units: Mapped[list["Unit"]] = relationship(back_populates="state")
    courts: Mapped[list["Court"]] = relationship(back_populates="state")


class District(Base):
    __tablename__ = "district"

    district_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    district_name: Mapped[str] = mapped_column(String(100), nullable=False)
    state_id: Mapped[int] = mapped_column(Integer, ForeignKey("state.state_id"), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    state: Mapped["State"] = relationship(back_populates="districts")
    units: Mapped[list["Unit"]] = relationship(back_populates="district")
    courts: Mapped[list["Court"]] = relationship(back_populates="district")
    employees: Mapped[list["Employee"]] = relationship(back_populates="district")  # noqa: F821


class UnitType(Base):
    __tablename__ = "unit_type"

    unit_type_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    unit_type_name: Mapped[str] = mapped_column(String(100), nullable=False)
    city_dist_state: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    hierarchy: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    units: Mapped[list["Unit"]] = relationship(back_populates="unit_type")


class Unit(Base):
    """Police station / circle / district office / range / state HQ hierarchy."""

    __tablename__ = "unit"

    unit_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    unit_name: Mapped[str] = mapped_column(String(150), nullable=False)
    type_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("unit_type.unit_type_id"), nullable=True)
    parent_unit: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("unit.unit_id"), nullable=True)
    nationality_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    state_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("state.state_id"), nullable=True)
    district_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("district.district_id"), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    unit_type: Mapped["UnitType"] = relationship(back_populates="units")
    parent: Mapped["Optional[Unit]"] = relationship(remote_side="Unit.unit_id", back_populates="children")
    children: Mapped[list["Unit"]] = relationship(back_populates="parent")
    state: Mapped["State"] = relationship(back_populates="units")
    district: Mapped["District"] = relationship(back_populates="units")

    employees: Mapped[list["Employee"]] = relationship(back_populates="unit")  # noqa: F821
    cases: Mapped[list["CaseMaster"]] = relationship(back_populates="police_station")  # noqa: F821


class Rank(Base):
    __tablename__ = "rank_master"

    rank_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rank_name: Mapped[str] = mapped_column(String(100), nullable=False)
    hierarchy: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    employees: Mapped[list["Employee"]] = relationship(back_populates="rank")  # noqa: F821


class Designation(Base):
    __tablename__ = "designation"

    designation_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    designation_name: Mapped[str] = mapped_column(String(100), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    sort_order: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    employees: Mapped[list["Employee"]] = relationship(back_populates="designation")  # noqa: F821


class CaseCategory(Base):
    __tablename__ = "case_category"

    case_category_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lookup_value: Mapped[str] = mapped_column(String(50), nullable=False)  # FIR, UDR, PAR, Zero FIR

    cases: Mapped[list["CaseMaster"]] = relationship(back_populates="case_category")  # noqa: F821


class GravityOffence(Base):
    __tablename__ = "gravity_offence"

    gravity_offence_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lookup_value: Mapped[str] = mapped_column(String(50), nullable=False)  # Heinous / Non-Heinous

    cases: Mapped[list["CaseMaster"]] = relationship(back_populates="gravity_offence")  # noqa: F821


class CrimeHead(Base):
    __tablename__ = "crime_head"

    crime_head_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    crime_group_name: Mapped[str] = mapped_column(String(150), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    sub_heads: Mapped[list["CrimeSubHead"]] = relationship(back_populates="crime_head")
    cases: Mapped[list["CaseMaster"]] = relationship(back_populates="crime_major_head")  # noqa: F821
    act_sections: Mapped[list["CrimeHeadActSection"]] = relationship(back_populates="crime_head")


class CrimeSubHead(Base):
    __tablename__ = "crime_sub_head"

    crime_sub_head_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    crime_head_id: Mapped[int] = mapped_column(Integer, ForeignKey("crime_head.crime_head_id"), nullable=False)
    crime_head_name: Mapped[str] = mapped_column(String(150), nullable=False)  # sub-head display name
    seq_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    crime_head: Mapped["CrimeHead"] = relationship(back_populates="sub_heads")
    cases: Mapped[list["CaseMaster"]] = relationship(back_populates="crime_minor_head")  # noqa: F821


class Act(Base):
    __tablename__ = "act"

    act_code: Mapped[str] = mapped_column(String(20), primary_key=True)
    act_description: Mapped[str] = mapped_column(String(255), nullable=False)
    short_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    sections: Mapped[list["Section"]] = relationship(back_populates="act")
    crime_head_links: Mapped[list["CrimeHeadActSection"]] = relationship(back_populates="act")
    case_links: Mapped[list["ActSectionAssociation"]] = relationship(back_populates="act")  # noqa: F821


class Section(Base):
    __tablename__ = "section"

    act_code: Mapped[str] = mapped_column(String(20), ForeignKey("act.act_code"), primary_key=True)
    section_code: Mapped[str] = mapped_column(String(20), primary_key=True)
    section_description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    act: Mapped["Act"] = relationship(back_populates="sections")
    crime_head_links: Mapped[list["CrimeHeadActSection"]] = relationship(
        back_populates="section", overlaps="act,crime_head_links"
    )
    case_links: Mapped[list["ActSectionAssociation"]] = relationship(  # noqa: F821
        back_populates="section", overlaps="act,case_links"
    )


class CrimeHeadActSection(Base):
    """Junction: which act/section combinations map to which crime head."""

    __tablename__ = "crime_head_act_section"

    crime_head_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("crime_head.crime_head_id"), primary_key=True
    )
    act_code: Mapped[str] = mapped_column(String(20), ForeignKey("act.act_code"), primary_key=True)
    section_code: Mapped[str] = mapped_column(String(20), primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(["act_code", "section_code"], ["section.act_code", "section.section_code"]),
    )

    crime_head: Mapped["CrimeHead"] = relationship(back_populates="act_sections")
    act: Mapped["Act"] = relationship(back_populates="crime_head_links", foreign_keys=[act_code])
    section: Mapped["Section"] = relationship(
        back_populates="crime_head_links",
        foreign_keys=[act_code, section_code],
        overlaps="act,crime_head_links",
    )


class CasteMaster(Base):
    __tablename__ = "caste_master"

    caste_master_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    caste_master_name: Mapped[str] = mapped_column(String(100), nullable=False)

    complainants: Mapped[list["ComplainantDetails"]] = relationship(back_populates="caste")  # noqa: F821


class ReligionMaster(Base):
    __tablename__ = "religion_master"

    religion_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    religion_name: Mapped[str] = mapped_column(String(100), nullable=False)

    complainants: Mapped[list["ComplainantDetails"]] = relationship(back_populates="religion")  # noqa: F821


class OccupationMaster(Base):
    __tablename__ = "occupation_master"

    occupation_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    occupation_name: Mapped[str] = mapped_column(String(100), nullable=False)

    complainants: Mapped[list["ComplainantDetails"]] = relationship(back_populates="occupation")  # noqa: F821


class CaseStatusMaster(Base):
    __tablename__ = "case_status_master"

    case_status_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_status_name: Mapped[str] = mapped_column(String(100), nullable=False)

    cases: Mapped[list["CaseMaster"]] = relationship(back_populates="case_status")  # noqa: F821


class Court(Base):
    __tablename__ = "court"

    court_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    court_name: Mapped[str] = mapped_column(String(150), nullable=False)
    district_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("district.district_id"), nullable=True)
    state_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("state.state_id"), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    district: Mapped["District"] = relationship(back_populates="courts")
    state: Mapped["State"] = relationship(back_populates="courts")
    cases: Mapped[list["CaseMaster"]] = relationship(back_populates="court")  # noqa: F821
