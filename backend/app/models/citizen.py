from sqlalchemy import CheckConstraint, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Citizen(Base):
    __tablename__ = "citizens"
    __table_args__ = (CheckConstraint("age >= 0 AND age <= 120", name="ck_citizens_age"),)

    citizen_id: Mapped[str] = mapped_column(String(12), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    district: Mapped[str] = mapped_column(String(100), nullable=False)
    demo_citizen_id: Mapped[str | None] = mapped_column(String(20), nullable=True)

    suspect_records: Mapped[list["Suspect"]] = relationship(back_populates="citizen")  # noqa: F821
    victim_records: Mapped[list["Victim"]] = relationship(back_populates="citizen")  # noqa: F821
    phones: Mapped[list["Phone"]] = relationship(back_populates="citizen")  # noqa: F821
    vehicles: Mapped[list["Vehicle"]] = relationship(back_populates="citizen")  # noqa: F821
    bank_accounts: Mapped[list["BankAccount"]] = relationship(back_populates="citizen")  # noqa: F821
