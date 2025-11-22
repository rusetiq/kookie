# Cookie Clicker

A full-featured Cookie Clicker game built with Flask and Supabase.

## Prerequisites

- Python 3.11+
- A Supabase project

## Database Setup

1.  Create a new Supabase project.
2.  Navigate to the "SQL Editor" in your Supabase project.
3.  Copy the contents of `schema.sql` and run it to create the necessary tables.

## API Reference

-   `POST /signup` - Create a new player account.
-   `POST /login` - Log in to a player account.
-   `GET /logout` - Log out of a player account.
-   `GET /api/saves` - Get all saves for the current player.
-   `POST /api/saves` - Create a new save.
-   `GET /api/saves/<save_id>` - Get a specific save.
-   `DELETE /api/saves/<save_id>` - Delete a specific save.
-   `GET /api/items` - Get all items in the shop.
-   `POST /api/buy` - Purchase an item.
-   `POST /api/clicks` - Add clicks to a save.
-   `GET /admin` - Admin panel (staff only).
-   `GET /admin/api/players` - Get all players (staff only).
-   `GET /admin/api/items` - Get all items (staff only).
-   `DELETE /admin/api/items/<item_id>` - Delete an item (staff only).
