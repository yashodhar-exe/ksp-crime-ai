from sqlalchemy import CHAR, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    account_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    citizen_id: Mapped[str] = mapped_column(String(12), ForeignKey("citizens.citizen_id"), nullable=False)
    bank_name: Mapped[str] = mapped_column(String(100), nullable=False)
    account_number: Mapped[str] = mapped_column(String(30), nullable=False)
    ifsc: Mapped[str | None] = mapped_column(CHAR(11), nullable=True)

    citizen: Mapped["Citizen"] = relationship(back_populates="bank_accounts")  # noqa: F821
