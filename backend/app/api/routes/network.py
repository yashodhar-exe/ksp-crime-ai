from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.citizen import Citizen
from app.models.user import User
from app.schemas.network import GraphEdge, GraphNode, NetworkGraphOut
from app.services import network_service

router = APIRouter(prefix="/network", tags=["network"])


@router.get("/{citizen_id}", response_model=NetworkGraphOut)
def get_network(
    citizen_id: str,
    depth: int = Query(default=1, ge=1, le=3),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> NetworkGraphOut:
    if db.get(Citizen, citizen_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Citizen not found")

    nodes, edges = network_service.build_network(db, citizen_id, depth=depth)

    return NetworkGraphOut(
        center=citizen_id,
        nodes=[GraphNode(id=n.citizen_id, label=f"{n.first_name} {n.last_name}") for n in nodes],
        edges=[
            GraphEdge(source=e.citizen_1, target=e.citizen_2, relationship_type=e.relationship_type) for e in edges
        ],
    )
