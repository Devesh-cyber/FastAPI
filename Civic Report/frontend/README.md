# Civic Report — Frontend

A React + Tailwind frontend for the Civic Report FastAPI backend. Citizens
register once, file complaints (garbage, potholes, water, drainage, etc.)
with a photo, and track them through a ticket-style status trail. There's
also a dashboard with stats and issue management for ward staff.

## Pages
- **Report** (`/`) — one-time citizen registration, then the issue form.
- **My reports** (`/my-reports`) — the current device's own reports.
- **Browse** (`/browse`) — public feed of all reports with filters.
- **Issue detail** (`/issues/:id`) — full ticket with a status timeline.
- **Dashboard** (`/dashboard`) — stats charts + manage status/delete.

## Setup

```bash
npm install
cp .env.example .env   # edit VITE_API_URL if your backend isn't on :8000
npm run dev
```

Open the printed local URL (usually `http://localhost:5173`).

## Connecting to the backend
The backend guards every write (create citizen, create/update/delete issue)
behind a fixed `api-key` header (see the backend's `auth.py`, default `123`).
There's no per-user login — everyone who knows the key can write. Enter it
once in the app (on the registration form, or in the Dashboard's "Access
key" field); it's cached in `localStorage` alongside your citizen profile.

Make sure the backend is started with the CORS + static file changes
described in the backend README/steps, otherwise the browser will block
API calls and photos won't load.
