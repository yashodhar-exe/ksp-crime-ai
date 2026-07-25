"""
Query-time semantic search over the FAISS index built by build_index.py.

Loads the same embedding backend that built the index (recorded in
vector_store/backend.txt) so query vectors live in the same space as the
indexed vectors. Everything is cached at module level after first use —
call reload() if you rebuild the index while the process is still running.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from embeddings import VECTOR_STORE_DIR, TFIDF_MODEL_PATH, get_backend  # noqa: E402

INDEX_PATH = VECTOR_STORE_DIR / "cases.index"
METADATA_PATH = VECTOR_STORE_DIR / "cases_metadata.csv"
BACKEND_MARKER_PATH = VECTOR_STORE_DIR / "backend.txt"

_index = None
_metadata: pd.DataFrame | None = None
_backend = None


class IndexNotBuiltError(RuntimeError):
    pass


def _ensure_loaded() -> None:
    global _index, _metadata, _backend
    if _index is not None:
        return

    if not (INDEX_PATH.exists() and METADATA_PATH.exists()):
        raise IndexNotBuiltError(
            "No RAG index found. Run `python ai/rag/build_index.py` first "
            "(after dataset/generator/generate_dataset.py has produced "
            "dataset/processed/*.csv)."
        )

    import faiss

    built_with = BACKEND_MARKER_PATH.read_text().strip() if BACKEND_MARKER_PATH.exists() else None
    _backend = get_backend(prefer=built_with) if built_with == "tfidf" else get_backend()
    _index = faiss.read_index(str(INDEX_PATH))
    _metadata = pd.read_csv(METADATA_PATH, dtype={"crime_no": str})


def reload() -> None:
    """Force a fresh load on the next search() call — use after rebuilding the index."""
    global _index, _metadata, _backend
    _index = None
    _metadata = None
    _backend = None


def is_available() -> bool:
    return INDEX_PATH.exists() and METADATA_PATH.exists()


def search(query: str, k: int = 5, exclude_case_master_id: int | None = None) -> list[dict]:
    """
    Returns up to `k` cases most semantically similar to `query`, each as:
        {case_master_id, crime_no, crime_head_name, district_name,
         case_status_name, brief_facts, score}
    Raises IndexNotBuiltError if build_index.py hasn't been run yet —
    callers (nlp_service.py, similarity_service.py) should catch this and
    fall back to keyword search.
    """
    _ensure_loaded()
    assert _index is not None and _metadata is not None and _backend is not None

    query_vector = _backend.encode([query])
    # fetch a few extra in case we need to drop the excluded case
    fetch_k = k + 1 if exclude_case_master_id is not None else k
    scores, indices = _index.search(query_vector, min(fetch_k, len(_metadata)))

    results = []
    for score, row_idx in zip(scores[0], indices[0]):
        if row_idx < 0:
            continue
        row = _metadata.iloc[row_idx]
        if exclude_case_master_id is not None and int(row["case_master_id"]) == exclude_case_master_id:
            continue
        results.append({
            "case_master_id": int(row["case_master_id"]),
            "crime_no": row["crime_no"],
            "crime_head_name": row["crime_head_name"] if pd.notna(row["crime_head_name"]) else None,
            "district_name": row["district_name"] if pd.notna(row["district_name"]) else None,
            "case_status_name": row["case_status_name"] if pd.notna(row["case_status_name"]) else None,
            "brief_facts": row["brief_facts"] if pd.notna(row["brief_facts"]) else "",
            "score": float(score),
        })
        if len(results) >= k:
            break
    return results
