import os
from textwrap import dedent

from flask import Flask, jsonify, render_template, request
from psycopg_pool import ConnectionPool

DATABASE_URL = os.getenv(
    "SUPABASE_DB_URL",
    "postgresql://postgres:Aarush1011@db.kteucjvbatzazvzzkags.supabase.co:5432/postgres",
)

pool = ConnectionPool(conninfo=DATABASE_URL, min_size=1, max_size=5, open=False)


def init_db() -> None:
    pool.open()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                dedent(
                    """
                    create table if not exists cookie_clicks (
                        player text primary key,
                        clicks bigint not null default 0,
                        updated_at timestamptz not null default now()
                    );
                    """
                )
            )


def get_clicks(player: str) -> int:
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "select clicks from cookie_clicks where player = %s",
                (player,),
            )
            row = cur.fetchone()
            if row is None:
                cur.execute(
                    "insert into cookie_clicks (player, clicks) values (%s, 0) returning clicks",
                    (player,),
                )
                row = cur.fetchone()
            return int(row[0])


def add_clicks(player: str, delta: int) -> int:
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                dedent(
                    """
                    insert into cookie_clicks (player, clicks)
                    values (%s, greatest(%s, 0))
                    on conflict (player) do update set
                        clicks = cookie_clicks.clicks + excluded.clicks,
                        updated_at = now()
                    returning clicks;
                    """
                ),
                (player, delta),
            )
            row = cur.fetchone()
            return int(row[0])


app = Flask(__name__)
init_db()


@app.get("/api/clicks")
def clicks_get():
    player = request.args.get("player", "default").strip() or "default"
    total = get_clicks(player)
    return jsonify({"player": player, "clicks": total})


@app.post("/api/clicks")
def clicks_post():
    data = request.get_json(silent=True) or {}
    player = (data.get("player") or "default").strip() or "default"
    delta = data.get("delta", 1)
    try:
        delta = int(delta)
    except (TypeError, ValueError):
        return jsonify({"error": "delta must be an integer"}), 400
    if delta <= 0:
        return jsonify({"error": "delta must be positive"}), 400
    total = add_clicks(player, delta)
    return jsonify({"player": player, "clicks": total})


@app.get("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
