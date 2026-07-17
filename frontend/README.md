# Frontend

React + TypeScript + Vite + Tailwind v4. Wired to every backend endpoint —
no mock data. Design tokens (colors, radii, typography) copied 1:1 from
`../docs/stitch-design-reference/police_analytics_design_system/DESIGN.md`
into `src/index.css`'s `@theme` block. The full Stitch export (all 17
screens' HTML/CSS + screenshots) is in that same folder for reference.

## Structure

- `src/api/` — one module per backend resource (`cases.ts`, `citizens.ts`,
  `search.ts`, `network.ts`, `dashboard.ts`, `chat.ts`, `officers.ts`,
  `stations.ts`, `analytics.ts`, `audit.ts`, `auth.ts`), plus `client.ts`
  (axios instance with JWT bearer + auto-refresh interceptor) and `jwt.ts`
  (client-side JWT payload decode for UI state only — the server verifies
  the signature on every request)
- `src/context/AuthContext.tsx` — login/logout, current user derived from
  the JWT payload
- `src/types/api.ts` — TypeScript types mirroring `backend/app/schemas/*.py`
  (kept in sync by hand — flag if backend schemas change)
- `src/types/roles.ts` — static mirror of `dataset/processed/roles.csv`
  for client-side permission checks (sidebar visibility, Settings page)
- `src/components/layout/` — Sidebar, Topbar, AppLayout, ProtectedRoute
- `src/components/ui/` — Icon (Material Symbols wrapper), Badge
  (priority/status pills), States (Loading/Error/Empty)
- `src/hooks/useAsync.ts` — small fetch-on-mount hook used by every page
  (deliberately simple — no react-query, this is hackathon-scale)
- `src/pages/` — one file per route; see `src/App.tsx` for the full route
  table

## Setup

```bash
npm install
cp .env.example .env   # set VITE_API_BASE_URL if backend isn't on :8000
npm run dev             # http://localhost:5173
```

## Build

```bash
npm run build   # tsc -b && vite build, output in dist/
```

## Notes on Stitch fidelity

Login and Dashboard pages directly reference the Stitch-exported HTML
layout. Other pages (Cases, Case Detail, Search, Citizen Profile, Network,
Officers, Stations, Analytics, Assistant, Audit, Users, Settings) use the
same design tokens and component vocabulary (cards, badges, the
`ai-panel` treatment for AI-generated content) but aren't a literal
pixel-for-pixel port of each individual Stitch screen file. See the root
README's "Honest scope notes" section.
