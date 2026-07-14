from pydantic import BaseModel


class SearchResultOut(BaseModel):
    entity_type: str
    entity_value: str
    case_id: str
    fir_number: str | None = None
    crime_type: str | None = None
    status: str | None = None


class SearchResponse(BaseModel):
    query: str
    entity_type: str | None
    results: list[SearchResultOut]
