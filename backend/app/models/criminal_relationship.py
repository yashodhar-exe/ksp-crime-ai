from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CriminalRelationship(Base):
    __tablename__ = "criminal_relationships"
    __table_args__ = (CheckConstraint("citizen_1 <> citizen_2", name="ck_criminal_rel_distinct"),)

    relationship_id: Mapped[str] = mapped_column(String(12), primary_key=True)
    citizen_1: Mapped[str] = mapped_column(String(12), ForeignKey("citizens.citizen_id"), nullable=False)
    citizen_2: Mapped[str] = mapped_column(String(12), ForeignKey("citizens.citizen_id"), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(50), nullable=False)

    citizen_one: Mapped["Citizen"] = relationship(foreign_keys=[citizen_1])  # noqa: F821
    citizen_two: Mapped["Citizen"] = relationship(foreign_keys=[citizen_2])  # noqa: F821
