# Cookie Clicker (Flask + Supabase)

A minimal Cookie Clicker backend built with Flask that persists click counts per player in a Supabase Postgres database. A basic vanilla JS page is included for quick testing.

## Prerequisites

- Python 3.11+
- Supabase Postgres connection string (provided via `SUPABASE_DB_URL`, defaults to the one shared in the prompt)

## API reference
- `GET /api/clicks?player=<name>` -> `{ "player": ..., "clicks": <int> }`
- `POST /api/clicks` with JSON `{ "player": "name", "delta": 1 }` -> updated count, validates positive integer delta.

## Notes
- Database table (`cookie_clicks`) is auto-created on startup if it does not exist.
- Connection pooling handled via `psycopg_pool.ConnectionPool` for efficiency.
