from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class InvestigationNote(Base):
    __tablename__ = "investigation_notes"

    note_id: Mapped[str] = mapped_column(String(12), primary_key=True)
    case_id: Mapped[str] = mapped_column(String(12), ForeignKey("cases.case_id"), nullable=False)
    officer_id: Mapped[str] = mapped_column(String(10), ForeignKey("officers.officer_id"), nullable=False)
    note: Mapped[str] = mapped_column(Text, nullable=False)

    case: Mapped["Case"] = relationship(back_populates="notes")  # noqa: F821
    officer: Mapped["Officer"] = relationship()  # noqa: F821
