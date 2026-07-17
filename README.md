# KSP Crime AI

Intelligent conversational AI platform for the Karnataka State Crime Records
Bureau (SCRB) — built for a Smart India Hackathon-style prototype. Lets
investigators query crime data using natural language and surface crime
patterns, criminal networks, socio-demographic insights, and early-warning
signals, instead of relying on static dashboards and manual queries.

## Problem Statement

SCRB manages crime data from 1,100+ police stations across Karnataka.
Current systems rely on static dashboards and manual queries, limiting deep
analysis and real-time insight. This project builds a conversational AI
layer on top of that data to enable:

- Crime pattern discovery
- Criminal network analysis
- Socio-demographic insights
- Behavioral profiling
- Proactive crime prevention intelligence

## Key Features

- Natural language chatbot (English; Kannada planned, not in MVP — see [Honest scope notes](#honest-scope-notes-on-this-build))
- Criminal network visualization
- Crime trend & hotspot detection (district-level; not GPS-based in MVP)
- Similar-case detection (crime_type + pattern_id matching, not a trained ML model)
- Explainable AI with audit trails
- Role-based secure access (Admin / SP / DSP / Inspector / Sub Inspector / Constable)

## Project Structure

```
ksp-crime-ai/
├── dataset/
│   ├── generator/       # scripts that produced the synthetic dataset
│   ├── raw/              # original, untouched CSVs
│   ├── processed/        # final CSVs — load these into Postgres
│   └── seed/              # load_database.py + schema.sql (DDL)
├── backend/               # FastAPI service — fully implemented, verified end-to-end
├── frontend/              # React + TypeScript + Tailwind — wired to every backend endpoint
├── ai/                    # notes on RAG / network analysis approach used inside backend/app/services
├── deployment/            # Dockerfiles + nginx config
├── scripts/               # dataset validation, demo password seeding
├── docs/                  # ER diagrams, API spec, roadmap
├── docker-compose.yml
├── .env.example
└── README.md
```

## Dataset

Synthetic but relationally consistent: 10,000 citizens, 10,000 cases, 500
officers, 100 stations, plus suspects, victims, evidence, digital evidence,
criminal relationships, timeline events, crime patterns, a real (not
random) search index, users, roles, and audit logs. See
`dataset/generator/` for how it was built and `scripts/validate_dataset.py`
for the integrity checks it passes.

Regenerate or re-validate:
```bash
python dataset/generator/generate_dataset.py
python dataset/generator/augment_dataset.py
python dataset/generator/augment_dataset_phase2.py
python scripts/validate_dataset.py
```

## Getting Started (Docker — recommended)

```bash
cp .env.example .env
docker compose up -d --build
psql postgresql://postgres:postgres@localhost:5433/ksp_crime -f dataset/seed/schema.sql
python dataset/seed/load_database.py
cd backend && alembic upgrade head && cd ..   # adds users.hashed_password — see backend/README.md
python scripts/seed_demo_passwords.py
```

- Backend: http://localhost:8000/docs (FastAPI's interactive Swagger UI)
- Frontend: http://localhost:3000

## Getting Started (local dev, no Docker)

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload   # http://localhost:8000

# Frontend (separate terminal)
cd frontend
npm install
cp .env.example .env
npm run dev                     # http://localhost:5173
```

Either way, run schema.sql + load_database.py + seed_demo_passwords.py
against your Postgres instance first (see Docker steps above for the exact
commands — same commands work locally, just point DATABASE_URL at
localhost:5433 or wherever your local Postgres is running).

## Demo Login

Passwords aren't part of the synthetic dataset — `dataset/processed/users.csv`
intentionally has no password column (see `scripts/seed_demo_passwords.py`
for why). After running that script, every seeded user shares one demo
password:

| Username | Role |
|---|---|
| `admin.scrb` | Admin |
| `sp.blr.city` | SP |
| `dsp.mysuru` | DSP |
| any of the 30 officer-linked usernames in `dataset/processed/users.csv` | Inspector / Sub Inspector / Constable |

**Password:** `Demo@KSP2026` (all users, all roles). This is a hackathon
demo credential — rotate it before any real deployment.

## Current Status

✅ Dataset complete and validated
✅ `dataset/seed/schema.sql` (Postgres DDL) — 19 tables, plus `hashed_password` on `users` for real auth
✅ FastAPI backend — full route set (auth, cases, citizens, search, network, analytics, chat, audit, users), verified end-to-end (login → JWT → protected endpoints → joined case data) against a live database
✅ Frontend — React + TypeScript + Tailwind, matching the Stitch design system's color tokens and component patterns, wired to every backend endpoint (no mock/hardcoded data)
⬜ Kannada language support
⬜ Trained similarity/ML model
⬜ GPS-based hotspot mapping (currently district-level only)

## Honest scope notes on this build

- **Frontend visual fidelity**: built against the Stitch design system's exact
  color tokens, typography, and component patterns (badges, cards, sidebar,
  AI-accent panels), and directly referenced the Stitch HTML for the
  Login and Dashboard layouts specifically. It is not a literal
  pixel-for-pixel port of all 17 exported Stitch screens — pages like
  Officers, Stations, and Users use a consistent, simpler table/card
  pattern rather than a full bespoke layout per screen.
- **AI Assistant**: `backend/app/services/nlp_service.py` uses full-text
  search over `complaint_text`/`investigation_notes` plus templated
  summarization — not a hosted LLM. This is disclosed in the UI, not
  hidden behind chatbot styling.
- **"Similar Cases"**: matched via `crime_type` + `pattern_id`, not a
  trained model. Labeled as such in the Case Detail page.
- **Network graph**: real SVG radial layout driven by live
  `criminal_relationships` data — not a canned demo image, but also not a
  physics-based force layout (didn't add a graph library dependency for a
  hackathon-scale network).
- **Every page under "Current Status" is wired to a real backend call** —
  verified by an end-to-end test (seed a user + case in a live DB, log in,
  hit protected endpoints, confirm real joined data comes back). There is
  no page in this frontend rendering hardcoded/mock JSON.

## Roadmap

1. ~~Postgres schema~~ — done
2. ~~FastAPI backend~~ — done, verified end-to-end
3. ~~Frontend~~ — done, wired to real backend, matches Stitch design tokens
4. **Polish**: Kannada support, GPS hotspots, trained similarity model,
   PDF export styling, deployment hardening (secrets management, rate
   limiting, HTTPS, moving off the demo password)

## License / Context

Built as a hackathon prototype (SIH-style problem statement). Not intended
for production use with real citizen data.
