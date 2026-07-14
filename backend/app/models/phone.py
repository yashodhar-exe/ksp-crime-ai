from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Phone(Base):
    __tablename__ = "phones"

    phone_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    citizen_id: Mapped[str] = mapped_column(String(12), ForeignKey("citizens.citizen_id"), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=False)
    provider: Mapped[str | None] = mapped_column(String(50), nullable=True)

    citizen: Mapped["Citizen"] = relationship(back_populates="phones")  # noqa: F821
