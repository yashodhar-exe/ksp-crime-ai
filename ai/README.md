# AI Layer

The AI/RAG logic ended up living in `backend/app/services/` rather than
here, since it's tightly coupled to the FastAPI request/response cycle and
the ORM models — splitting it into a separate top-level package added an
import boundary without a real benefit at this scale. See:

- `backend/app/services/nlp_service.py` — chat query handling; currently
  full-text search over `cases.complaint_text` (Postgres GIN index) +
  templated summarization, with a documented seam for swapping in a real
  LLM/vector DB later
- `backend/app/services/similarity_service.py` — "similar cases" via
  `crime_type` + `pattern_id` matching
- `backend/app/services/chat_store.py` — in-process chat history storage
  (swap for a `chat_sessions`/`chat_messages` table for persistence
  across restarts)

This folder is kept as a placeholder for genuinely separable future work:
- `rag/` — if/when embeddings + a vector DB replace the full-text fallback
- `translation/` — Kannada support (not built — see root README)
- `network_analysis/` — the citizen relationship graph is currently built
  directly in `backend/app/services/` off `criminal_relationships`; would
  move here if it grows into something reused outside the API (e.g. a
  batch job)
