import os

from flask import Flask, jsonify, render_template, request
from supabase import Client, create_client

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://kteucjvbatzazvzzkags.supabase.co")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_SERVICE_KEY")
if not SUPABASE_SERVICE_KEY:
    raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY (or SUPABASE_SERVICE_KEY) must be set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
TABLE_NAME = "cookie_clicks"


def fetch_clicks(player: str) -> int | None:
    response = (
        supabase.table(TABLE_NAME)
        .select("clicks")
        .eq("player", player)
        .limit(1)
        .execute()
    )
    rows = response.data or []
    return int(rows[0]["clicks"]) if rows else None


def ensure_player(player: str) -> int:
    clicks = fetch_clicks(player)
    if clicks is not None:
        return clicks
    supabase.table(TABLE_NAME).insert({"player": player, "clicks": 0}).execute()
    return 0


def persist_clicks(player: str, clicks: int) -> int:
    supabase.table(TABLE_NAME).upsert({"player": player, "clicks": clicks}).execute()
    return clicks


def get_clicks(player: str) -> int:
    return ensure_player(player)


def add_clicks(player: str, delta: int) -> int:
    current = ensure_player(player)
    total = current + delta
    return persist_clicks(player, total)


app = Flask(__name__)


@app.get("/api/clicks")
def clicks_get():
    player = request.args.get("player", "default").strip() or "default"
    try:
        total = get_clicks(player)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
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
    try:
        total = add_clicks(player, delta)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
    return jsonify({"player": player, "clicks": total})


@app.get("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
