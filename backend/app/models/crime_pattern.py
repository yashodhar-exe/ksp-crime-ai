from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CrimePattern(Base):
    __tablename__ = "crime_patterns"

    pattern_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    crime_type: Mapped[str] = mapped_column(String(50), nullable=False)
    modus_operandi: Mapped[str | None] = mapped_column(String(150), nullable=True)
    communication: Mapped[str | None] = mapped_column(String(50), nullable=True)
    payment_method: Mapped[str | None] = mapped_column(String(50), nullable=True)
    risk_level: Mapped[str] = mapped_column(String(20), nullable=False)

    cases: Mapped[list["Case"]] = relationship(back_populates="pattern")  # noqa: F821
