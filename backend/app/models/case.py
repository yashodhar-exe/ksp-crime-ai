from datetime import date

from sqlalchemy import BigInteger, Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Case(Base):
    __tablename__ = "cases"

    case_id: Mapped[str] = mapped_column(String(12), primary_key=True)
    fir_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    crime_type: Mapped[str] = mapped_column(String(50), nullable=False)
    station_id: Mapped[str] = mapped_column(String(10), ForeignKey("police_stations.station_id"), nullable=False)
    officer_id: Mapped[str] = mapped_column(String(10), ForeignKey("officers.officer_id"), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    priority: Mapped[str] = mapped_column(String(20), nullable=False)
    incident_date: Mapped[date] = mapped_column(Date, nullable=False)
    registered_date: Mapped[date] = mapped_column(Date, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    district: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    estimated_loss: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
    complaint_text: Mapped[str] = mapped_column(Text, nullable=False)
    pattern_id: Mapped[str | None] = mapped_column(String(10), ForeignKey("crime_patterns.pattern_id"), nullable=True)

    station: Mapped["PoliceStation"] = relationship(back_populates="cases")  # noqa: F821
    officer: Mapped["Officer"] = relationship(back_populates="cases")  # noqa: F821
    pattern: Mapped["CrimePattern | None"] = relationship(back_populates="cases")  # noqa: F821

    suspects: Mapped[list["Suspect"]] = relationship(back_populates="case")  # noqa: F821
    victims: Mapped[list["Victim"]] = relationship(back_populates="case")  # noqa: F821
    evidence: Mapped[list["Evidence"]] = relationship(back_populates="case")  # noqa: F821
    digital_evidence: Mapped[list["DigitalEvidence"]] = relationship(back_populates="case")  # noqa: F821
    notes: Mapped[list["InvestigationNote"]] = relationship(back_populates="case")  # noqa: F821
    timeline_events: Mapped[list["TimelineEvent"]] = relationship(back_populates="case")  # noqa: F821
