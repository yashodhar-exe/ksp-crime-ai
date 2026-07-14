"""
Declarative base for all ORM models. Kept separate from session.py so that
alembic (or any script) can `from app.db.base import Base` without pulling
in the engine / connection machinery.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
