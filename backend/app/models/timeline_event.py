from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TimelineEvent(Base):
    __tablename__ = "timeline"

    event_id: Mapped[str] = mapped_column(String(12), primary_key=True)
    case_id: Mapped[str] = mapped_column(String(12), ForeignKey("cases.case_id"), nullable=False)
    event: Mapped[str] = mapped_column(String(200), nullable=False)

    case: Mapped["Case"] = relationship(back_populates="timeline_events")  # noqa: F821
