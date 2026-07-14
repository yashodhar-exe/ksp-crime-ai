from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.citizen import Citizen
from app.models.criminal_relationship import CriminalRelationship


def build_network(db: Session, citizen_id: str, depth: int = 1) -> tuple[list[Citizen], list[CriminalRelationship]]:
    """
    Builds a small node/edge graph centered on `citizen_id`, expanding
    `depth` hops through criminal_relationships. depth=1 (default) returns
    the citizen's direct connections only — enough for the MVP network
    visualization; deeper traversal is a simple BFS extension here later.
    """
    visited_ids: set[str] = {citizen_id}
    frontier: set[str] = {citizen_id}
    all_edges: list[CriminalRelationship] = []

    for _ in range(max(depth, 1)):
        if not frontier:
            break
        stmt = select(CriminalRelationship).where(
            or_(
                CriminalRelationship.citizen_1.in_(frontier),
                CriminalRelationship.citizen_2.in_(frontier),
            )
        )
        edges = db.execute(stmt).scalars().all()
        next_frontier: set[str] = set()
        for edge in edges:
            all_edges.append(edge)
            for cid in (edge.citizen_1, edge.citizen_2):
                if cid not in visited_ids:
                    next_frontier.add(cid)
        visited_ids |= next_frontier
        frontier = next_frontier

    if not visited_ids:
        return [], []

    nodes_stmt = select(Citizen).where(Citizen.citizen_id.in_(visited_ids))
    nodes = db.execute(nodes_stmt).scalars().all()

    # de-dupe edges (a node reachable via two hops could produce repeats)
    unique_edges = {edge.relationship_id: edge for edge in all_edges}

    return list(nodes), list(unique_edges.values())
