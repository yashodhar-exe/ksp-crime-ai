from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Evidence(Base):
    __tablename__ = "evidence"

    evidence_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    case_id: Mapped[str] = mapped_column(String(12), ForeignKey("cases.case_id"), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    collected_by: Mapped[str | None] = mapped_column(String(10), ForeignKey("officers.officer_id"), nullable=True)

    case: Mapped["Case"] = relationship(back_populates="evidence")  # noqa: F821
    collected_by_officer: Mapped["Officer | None"] = relationship()  # noqa: F821
