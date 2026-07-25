"""
Embedding backend for the RAG layer, with automatic graceful degradation.

Preferred path: sentence-transformers/all-MiniLM-L6-v2 (384-dim, downloaded
from the HuggingFace Hub on first use, cached locally after that). This is
what should run in any environment with normal internet access.

Fallback path: a TF-IDF + TruncatedSVD "embedding" (scikit-learn, no model
download, fully offline). Lower semantic quality than MiniLM, but a real,
working local vector representation — used automatically if MiniLM can't
be loaded (e.g. no internet access, or the model isn't cached yet and the
network is unreachable).

Both backends expose the same interface (`fit`/`transform`/`encode`), so
build_index.py and search.py don't need to know which one is active.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

import numpy as np

logger = logging.getLogger(__name__)

VECTOR_STORE_DIR = Path(__file__).parent / "vector_store"
TFIDF_MODEL_PATH = VECTOR_STORE_DIR / "tfidf_backend.joblib"

BackendName = Literal["minilm", "tfidf"]

_MINILM_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_TFIDF_DIMS = 384  # match MiniLM's dim so downstream FAISS config doesn't care which backend built the index


class EmbeddingBackend:
    """Common interface both backends implement."""

    name: BackendName
    dims: int

    def encode(self, texts: list[str]) -> np.ndarray:
        raise NotImplementedError


class MiniLMBackend(EmbeddingBackend):
    name = "minilm"
    dims = 384

    def __init__(self):
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer(_MINILM_MODEL_NAME)

    def encode(self, texts: list[str]) -> np.ndarray:
        vectors = self._model.encode(
            texts, normalize_embeddings=True, show_progress_bar=False, convert_to_numpy=True
        )
        return vectors.astype("float32")


class TfidfBackend(EmbeddingBackend):
    """
    TF-IDF (up to bigrams) -> TruncatedSVD(384) -> L2-normalize. This is a
    legitimate, working local semantic-ish representation (captures shared
    vocabulary/topic overlap via LSA), just weaker than a transformer
    encoder at paraphrase-level matching. It has no external dependency
    beyond scikit-learn, so it always works.
    """

    name = "tfidf"
    dims = _TFIDF_DIMS

    def __init__(self, fitted_path: Path | None = None):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.decomposition import TruncatedSVD
        from sklearn.pipeline import Pipeline

        if fitted_path and fitted_path.exists():
            import joblib

            self._pipeline: Pipeline = joblib.load(fitted_path)
            self._fitted = True
        else:
            self._pipeline = Pipeline([
                ("tfidf", TfidfVectorizer(max_features=20_000, ngram_range=(1, 2), min_df=1, stop_words="english")),
                ("svd", TruncatedSVD(n_components=self.dims, random_state=42)),
            ])
            self._fitted = False

    def fit(self, texts: list[str]) -> np.ndarray:
        vectors = self._pipeline.fit_transform(texts)
        self._fitted = True
        return self._normalize(vectors)

    def encode(self, texts: list[str]) -> np.ndarray:
        if not self._fitted:
            raise RuntimeError("TfidfBackend must be fit (via build_index.py) before encoding queries.")
        vectors = self._pipeline.transform(texts)
        return self._normalize(vectors)

    def save(self, path: Path) -> None:
        import joblib

        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self._pipeline, path)

    @staticmethod
    def _normalize(vectors: np.ndarray) -> np.ndarray:
        vectors = np.asarray(vectors, dtype="float32")
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return vectors / norms


def get_backend(prefer: BackendName | None = None) -> EmbeddingBackend:
    """
    Returns the best available backend. Tries MiniLM first (unless
    `prefer="tfidf"` is forced, e.g. for offline CI), falls back to TF-IDF
    (loading a previously-fit vectorizer if one exists) on any failure —
    missing package, no internet, HF Hub unreachable, etc.
    """
    if prefer == "tfidf":
        return TfidfBackend(fitted_path=TFIDF_MODEL_PATH)

    try:
        return MiniLMBackend()
    except Exception as exc:  # noqa: BLE001 - deliberately broad: any failure means "fall back"
        logger.warning(
            "Falling back to the offline TF-IDF embedding backend "
            "(MiniLM unavailable: %s). Semantic search will still work, "
            "just with lower-quality matching than a transformer encoder.",
            exc,
        )
        return TfidfBackend(fitted_path=TFIDF_MODEL_PATH)
