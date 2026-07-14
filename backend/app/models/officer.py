from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Officer(Base):
    __tablename__ = "officers"

    officer_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    rank: Mapped[str] = mapped_column(String(50), nullable=False)
    station_id: Mapped[str] = mapped_column(String(10), ForeignKey("police_stations.station_id"), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)

    station: Mapped["PoliceStation"] = relationship(back_populates="officers")  # noqa: F821
    cases: Mapped[list["Case"]] = relationship(back_populates="officer")  # noqa: F821
