from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Victim(Base):
    __tablename__ = "victims"

    victim_id: Mapped[str] = mapped_column(String(12), primary_key=True)
    case_id: Mapped[str] = mapped_column(String(12), ForeignKey("cases.case_id"), nullable=False)
    citizen_id: Mapped[str] = mapped_column(String(12), ForeignKey("citizens.citizen_id"), nullable=False)
    injury_level: Mapped[str] = mapped_column(String(30), nullable=False)

    case: Mapped["Case"] = relationship(back_populates="victims")  # noqa: F821
    citizen: Mapped["Citizen"] = relationship(back_populates="victim_records")  # noqa: F821
