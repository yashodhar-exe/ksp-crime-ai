from pydantic import BaseModel


class GraphNode(BaseModel):
    id: str
    label: str
    type: str = "citizen"


class GraphEdge(BaseModel):
    source: str
    target: str
    relationship_type: str


class NetworkGraphOut(BaseModel):
    center: str
    nodes: list[GraphNode]
    edges: list[GraphEdge]
