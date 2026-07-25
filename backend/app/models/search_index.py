from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class SearchIndex(Base):
    __tablename__ = "search_index"

    search_id: Mapped[str] = mapped_column(String(12), primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(20), nullable=False)  # Citizen | Phone | Vehicle | Bank | Officer | Case
    entity_value: Mapped[str] = mapped_column(String(100), nullable=False)
    case_id: Mapped[str] = mapped_column(String(12), nullable=False)
