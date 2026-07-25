from __future__ import annotations

from sqlalchemy import ForeignKey, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ActSectionAssociation(Base):
    """Which acts/sections are invoked for a given FIR, in print order."""

    __tablename__ = "act_section_association"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_master_id: Mapped[int] = mapped_column(Integer, ForeignKey("case_master.case_master_id"), nullable=False)
    act_id: Mapped[str] = mapped_column(String(20), ForeignKey("act.act_code"), nullable=False)
    section_id: Mapped[str] = mapped_column(String(20), nullable=False)
    act_order_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    section_order_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(["act_id", "section_id"], ["section.act_code", "section.section_code"]),
    )

    case: Mapped["CaseMaster"] = relationship(back_populates="act_sections")  # noqa: F821
    act: Mapped["Act"] = relationship(back_populates="case_links", foreign_keys=[act_id])  # noqa: F821
    section: Mapped["Section"] = relationship(  # noqa: F821
        back_populates="case_links",
        foreign_keys=[act_id, section_id],
        overlaps="act,case_links",
    )
