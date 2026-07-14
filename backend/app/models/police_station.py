from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class PoliceStation(Base):
    __tablename__ = "police_stations"

    station_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    station_name: Mapped[str] = mapped_column(String(150), nullable=False)
    district: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)

    officers: Mapped[list["Officer"]] = relationship(back_populates="station")  # noqa: F821
    cases: Mapped[list["Case"]] = relationship(back_populates="station")  # noqa: F821
