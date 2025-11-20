# Cookie Clicker

A minimal Cookie Clicker backend built with Flask that persists click counts per player in a Supabase Postgres database via the official Supabase Python client. A basic vanilla JS page is included for quick testing.

## Prerequisites

- Python 3.11+

## API reference
- `GET /api/clicks?player=<name>` -> `{ "player": ..., "clicks": <int> }`
- `POST /api/clicks` with JSON `{ "player": "name", "delta": 1 }` -> updated count, validates positive integer delta.

## Notes
- Supabase operations are performed through the official client using the service-role key for convenience.
- Increment logic is intentionally simple; concurrent writes may last-write-wins. For heavier usage consider a single `update` with SQL or RPC.
