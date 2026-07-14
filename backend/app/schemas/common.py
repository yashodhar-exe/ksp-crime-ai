from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    """Base for response schemas that read straight off SQLAlchemy models."""

    model_config = ConfigDict(from_attributes=True)


class Page(BaseModel):
    total: int
    limit: int
    offset: int
