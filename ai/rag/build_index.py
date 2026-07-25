"""
Builds a FAISS vector index over every case's narrative (brief_facts,
enriched with crime head/sub-head, district, and act/section context so
the embedding captures more than just the free-text complaint).

Usage:
    python ai/rag/build_index.py                  # auto: MiniLM if available, else TF-IDF
    python ai/rag/build_index.py --backend tfidf   # force the offline backend

Reads from dataset/processed/*.csv (run dataset/generator/generate_dataset.py
first if these don't exist yet). Writes:
    ai/rag/vector_store/cases.index          — FAISS index
    ai/rag/vector_store/cases_metadata.csv   — case_master_id, crime_no, and
                                                display fields aligned by row
                                                position with the FAISS index
    ai/rag/vector_store/tfidf_backend.joblib — only written when using the
                                                TF-IDF backend, so search.py
                                                can load the *same* fitted
                                                vectorizer/SVD at query time
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from embeddings import VECTOR_STORE_DIR, TFIDF_MODEL_PATH, TfidfBackend, get_backend  # noqa: E402

DATASET_DIR = Path(__file__).parent.parent.parent / "dataset" / "processed"
INDEX_PATH = VECTOR_STORE_DIR / "cases.index"
METADATA_PATH = VECTOR_STORE_DIR / "cases_metadata.csv"


def _load_case_documents() -> pd.DataFrame:
    cases = pd.read_csv(DATASET_DIR / "case_master.csv", dtype={"crime_no": str, "case_no": str})
    crime_sub_head = pd.read_csv(DATASET_DIR / "crime_sub_head.csv")
    crime_head = pd.read_csv(DATASET_DIR / "crime_head.csv")
    unit = pd.read_csv(DATASET_DIR / "unit.csv")
    district = pd.read_csv(DATASET_DIR / "district.csv")
    case_status = pd.read_csv(DATASET_DIR / "case_status_master.csv")
    act_section = pd.read_csv(DATASET_DIR / "act_section_association.csv")

    df = cases.merge(crime_sub_head, left_on="crime_minor_head_id", right_on="crime_sub_head_id", how="left")
    df = df.merge(crime_head, left_on="crime_head_id", right_on="crime_head_id", how="left", suffixes=("", "_head"))
    df = df.merge(unit, left_on="police_station_id", right_on="unit_id", how="left")
    df = df.merge(district, left_on="district_id", right_on="district_id", how="left")
    df = df.merge(case_status, left_on="case_status_id", right_on="case_status_id", how="left")

    act_sections_by_case = (
        act_section.assign(cite=lambda d: d["act_id"] + " " + d["section_id"])
        .groupby("case_master_id")["cite"]
        .apply(lambda s: ", ".join(s))
    )
    df["act_sections_text"] = df["case_master_id"].map(act_sections_by_case).fillna("")

    def build_doc(row) -> str:
        parts = [
            f"Crime {row['crime_no']}.",
            f"{row.get('crime_head_name', 'Unclassified')} — {row.get('crime_group_name', '')}."
            if pd.notna(row.get("crime_head_name")) else "",
            f"Registered at {row.get('unit_name', 'unknown station')}, {row.get('district_name', 'unknown district')}.",
            f"Sections: {row['act_sections_text']}." if row["act_sections_text"] else "",
            f"Status: {row.get('case_status_name', 'unknown')}.",
            str(row.get("brief_facts") or ""),
        ]
        return " ".join(p for p in parts if p)

    df["document"] = df.apply(build_doc, axis=1)
    return df[["case_master_id", "crime_no", "crime_head_name", "district_name", "case_status_name", "brief_facts", "document"]]


def build(backend_name: str | None) -> None:
    import faiss

    print("Loading case documents from dataset/processed/ ...")
    df = _load_case_documents()
    print(f"  {len(df)} cases")

    prefer = "tfidf" if backend_name == "tfidf" else None
    backend = get_backend(prefer=prefer)
    print(f"Embedding backend: {backend.name}")

    texts = df["document"].tolist()
    if isinstance(backend, TfidfBackend):
        vectors = backend.fit(texts)
        backend.save(TFIDF_MODEL_PATH)
        print(f"  saved fitted TF-IDF/SVD pipeline -> {TFIDF_MODEL_PATH}")
    else:
        vectors = backend.encode(texts)

    print(f"Embedded {vectors.shape[0]} cases into {vectors.shape[1]}-dim vectors")

    index = faiss.IndexFlatIP(vectors.shape[1])  # inner product on normalized vectors == cosine similarity
    index.add(vectors)

    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))
    df.drop(columns=["document"]).to_csv(METADATA_PATH, index=False)

    # record which backend built this index so search.py can match it
    (VECTOR_STORE_DIR / "backend.txt").write_text(backend.name)

    print(f"Wrote index -> {INDEX_PATH}")
    print(f"Wrote metadata -> {METADATA_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=["minilm", "tfidf"], default=None,
                         help="Force a specific backend; default auto-detects (MiniLM if reachable, else TF-IDF).")
    args = parser.parse_args()
    build(args.backend)
