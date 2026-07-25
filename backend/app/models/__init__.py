"""
Import every model here so that (a) `Base.metadata` sees all tables for
Alembic autogeneration, and (b) SQLAlchemy can resolve the string-based
relationship() references between files regardless of import order.
"""
from app.db.base import Base  # noqa: F401

from app.models.role import Role  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.audit_log import AuditLog  # noqa: F401

# New CaseMaster Schema Models
from app.models.lookups import (
    State, District, UnitType, Unit, Rank, Designation,
    Court, CaseCategory, GravityOffence, CrimeHead,
    CrimeSubHead, CaseStatusMaster, Act, Section,
    CrimeHeadActSection, OccupationMaster, ReligionMaster, CasteMaster
)  # noqa: F401
from app.models.employee import Employee  # noqa: F401
from app.models.case_master import CaseMaster  # noqa: F401
from app.models.complainant import ComplainantDetails  # noqa: F401
from app.models.victim import Victim  # noqa: F401
from app.models.accused import Accused  # noqa: F401
from app.models.act_section_association import ActSectionAssociation  # noqa: F401
from app.models.arrest_surrender import ArrestSurrender  # noqa: F401
from app.models.chargesheet import ChargesheetDetails  # noqa: F401

__all__ = [
    "Base",
    "Role",
    "User",
    "AuditLog",
    # New CaseMaster Schema
    "State", "District", "UnitType", "Unit", "Rank", "Designation",
    "Court", "CaseCategory", "GravityOffence", "CrimeHead",
    "CrimeSubHead", "CaseStatusMaster", "Act", "Section",
    "CrimeHeadActSection", "OccupationMaster", "ReligionMaster", "CasteMaster",
    "Employee", "CaseMaster", "ComplainantDetails", "Victim", "Accused",
    "ActSectionAssociation", "ArrestSurrender", "ChargesheetDetails"
]
