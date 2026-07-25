from typing import Optional
from pydantic import BaseModel


class SearchResultOut(BaseModel):
    entity_type: str
    entity_value: str
    case_id: str
    fir_number: Optional[str] = None
    crime_type: Optional[str] = None
    status: Optional[str] = None


class SearchResponse(BaseModel):
    query: str
    entity_type: Optional[str]
    results: list[SearchResultOut]
