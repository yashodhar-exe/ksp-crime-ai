from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    vehicle_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    citizen_id: Mapped[str] = mapped_column(String(12), ForeignKey("citizens.citizen_id"), nullable=False)
    vehicle_number: Mapped[str] = mapped_column(String(20), nullable=False)
    vehicle_type: Mapped[str | None] = mapped_column(String(30), nullable=True)

    citizen: Mapped["Citizen"] = relationship(back_populates="vehicles")  # noqa: F821
