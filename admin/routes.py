from functools import wraps

from flask import Blueprint, jsonify, render_template, request, session

from database import supabase

admin_bp = Blueprint("admin", __name__)


# Admin Panel
def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_staff"):
            return "Unauthorized", 401
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route("/admin")
@staff_required
def admin():
    return render_template("admin.html")


@admin_bp.get("/admin/api/players")
@staff_required
def admin_get_players():
    response = supabase.table("players").select("*, saves(*)").execute()
    return jsonify(response.data)


@admin_bp.get("/admin/api/items")
@staff_required
def admin_get_items():
    response = supabase.table("items").select("*").execute()
    return jsonify(response.data)


@admin_bp.delete("/admin/api/items/<item_id>")
@staff_required
def admin_delete_item(item_id):
    supabase.table("items").delete().eq("id", item_id).execute()
    return "Item deleted", 200


@admin_bp.get("/admin/api/players/<player_id>")
@staff_required
def admin_get_player(player_id):
    response = supabase.table("players").select("*, saves(*)").eq("id", player_id).execute()
    if not response.data:
        return "Player not found", 404
    return jsonify(response.data[0])


@admin_bp.put("/admin/api/players/<player_id>")
@staff_required
def admin_update_player(player_id):
    data = request.get_json()
    for save in data["saves"]:
        supabase.table("saves").update({"cookies": save["cookies"]}).eq("id", save["id"]).execute()
    return "Player updated", 200


@admin_bp.post("/admin/api/items")
@staff_required
def admin_create_item():
    data = request.get_json()
    supabase.table("items").insert(data).execute()
    return "Item created", 201


@admin_bp.get("/admin/api/items/<item_id>")
@staff_required
def admin_get_item(item_id):
    response = supabase.table("items").select("*").eq("id", item_id).execute()
    if not response.data:
        return "Item not found", 404
    return jsonify(response.data[0])


@admin_bp.put("/admin/api/items/<item_id>")
@staff_required
def admin_update_item(item_id):
    data = request.get_json()
    supabase.table("items").update(data).eq("id", item_id).execute()
    return "Item updated", 200
