"""
Import every model here so that (a) `Base.metadata` sees all tables for
Alembic autogeneration, and (b) SQLAlchemy can resolve the string-based
relationship() references between files regardless of import order.
"""
from app.db.base import Base  # noqa: F401

from app.models.police_station import PoliceStation  # noqa: F401
from app.models.role import Role  # noqa: F401
from app.models.citizen import Citizen  # noqa: F401
from app.models.officer import Officer  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.crime_pattern import CrimePattern  # noqa: F401
from app.models.case import Case  # noqa: F401
from app.models.suspect import Suspect  # noqa: F401
from app.models.victim import Victim  # noqa: F401
from app.models.phone import Phone  # noqa: F401
from app.models.vehicle import Vehicle  # noqa: F401
from app.models.bank_account import BankAccount  # noqa: F401
from app.models.evidence import Evidence  # noqa: F401
from app.models.digital_evidence import DigitalEvidence  # noqa: F401
from app.models.criminal_relationship import CriminalRelationship  # noqa: F401
from app.models.investigation_note import InvestigationNote  # noqa: F401
from app.models.timeline_event import TimelineEvent  # noqa: F401
from app.models.search_index import SearchIndex  # noqa: F401
from app.models.audit_log import AuditLog  # noqa: F401

__all__ = [
    "Base",
    "PoliceStation",
    "Role",
    "Citizen",
    "Officer",
    "User",
    "CrimePattern",
    "Case",
    "Suspect",
    "Victim",
    "Phone",
    "Vehicle",
    "BankAccount",
    "Evidence",
    "DigitalEvidence",
    "CriminalRelationship",
    "InvestigationNote",
    "TimelineEvent",
    "SearchIndex",
    "AuditLog",
]
