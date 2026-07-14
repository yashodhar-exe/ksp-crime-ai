from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class DigitalEvidence(Base):
    __tablename__ = "digital_evidence"

    digital_evidence_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    case_id: Mapped[str] = mapped_column(String(12), ForeignKey("cases.case_id"), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)
    file_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(15), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    uploaded_by: Mapped[str | None] = mapped_column(String(10), ForeignKey("officers.officer_id"), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    extracted_entities: Mapped[str | None] = mapped_column(Text, nullable=True)

    case: Mapped["Case"] = relationship(back_populates="digital_evidence")  # noqa: F821
    uploaded_by_officer: Mapped["Officer | None"] = relationship()  # noqa: F821
