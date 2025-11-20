# Cookie Clicker (Flask + Supabase)

A minimal Cookie Clicker backend built with Flask that persists click counts per player in a Supabase Postgres database via the official Supabase Python client. A basic vanilla JS page is included for quick testing.

## Prerequisites

- Python 3.11+
- Supabase Postgres connection string (provided via `SUPABASE_DB_URL`, defaults to the one shared in the prompt)

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file (or set shell vars) with your Supabase project details:

```
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_SERVICE_ROLE_KEY=ey...
```

The service-role key is required because the API performs unrestricted inserts/updates. Keep it private.

Ensure the `cookie_clicks` table exists in your Supabase database (run once in the SQL editor):

```sql
create table if not exists public.cookie_clicks (
  player text primary key,
  clicks bigint not null default 0,
  updated_at timestamptz not null default now()
);
```

## Running the app

```bash
set FLASK_APP=app
flask run --reload
```

Then open http://127.0.0.1:5000/ to click cookies.

## API reference
- `GET /api/clicks?player=<name>` -> `{ "player": ..., "clicks": <int> }`
- `POST /api/clicks` with JSON `{ "player": "name", "delta": 1 }` -> updated count, validates positive integer delta.

## Notes
- Supabase operations are performed through the official client using the service-role key for convenience.
- Increment logic is intentionally simple; concurrent writes may last-write-wins. For heavier usage consider a single `update` with SQL or RPC.
