from datetime import datetime, timezone

from flask import Blueprint, jsonify, request, session

from database import supabase

game_api_bp = Blueprint("game_api", __name__)


@game_api_bp.get("/api/items")
def get_items():
    response = supabase.table("items").select("*").execute()
    return jsonify(response.data)


@game_api_bp.post("/api/buy")
def buy_item():
    data = request.get_json()
    item_id = data["item_id"]
    save_id = data["save_id"]

    # Get the item from the database
    response = supabase.table("items").select("*").eq("id", item_id).execute()
    if not response.data:
        return "Item not found", 404
    item = response.data[0]

    # Get the player's save from the database
    response = supabase.table("saves").select("*").eq("id", save_id).execute()
    if not response.data:
        return "Save not found", 404
    save = response.data[0]

    # Calculate the cost of the item
    cost = item["cost"]
    if item["name"] == "Robot":
        response = supabase.table("inventory").select("quantity").eq("save_id", save_id).eq("item_id", item_id).execute()
        if response.data:
            quantity = response.data[0]["quantity"]
            cost = int(cost * (1.2 ** quantity))

    # Check if the player has enough cookies
    if save["cookies"] < cost:
        return "Not enough cookies", 400

    # Subtract the cost of the item
    new_cookies = save["cookies"] - cost
    supabase.table("saves").update({"cookies": new_cookies}).eq("id", save_id).execute()

    # Add the item to the player's inventory
    response = supabase.table("inventory").select("id, quantity").eq("save_id", save_id).eq("item_id", item_id).execute()
    if response.data:
        inventory_id = response.data[0]["id"]
        new_quantity = response.data[0]["quantity"] + 1
        supabase.table("inventory").update({"quantity": new_quantity}).eq("id", inventory_id).execute()
    else:
        supabase.table("inventory").insert({
            "save_id": save_id,
            "item_id": item_id,
        }).execute()

    return "Item purchased", 200


@game_api_bp.post("/api/clicks")
def add_clicks():
    data = request.get_json()
    save_id = data["save_id"]
    clicks = data["clicks"]

    # Get the player's save from the database
    response = supabase.table("saves").select("*").eq("id", save_id).execute()
    if not response.data:
        return "Save not found", 404
    save = response.data[0]

    # Get the player's inventory
    response = supabase.table("inventory").select("*, items(*)").eq("save_id", save_id).execute()
    inventory = response.data

    # Calculate the multiplier
    multiplier = 1
    for item in inventory:
        if item["items"]["effect"]["type"] == "multiplier":
            multiplier += item["items"]["effect"]["value"] * item["quantity"]

    # Update the cookie count
    new_cookies = save["cookies"] + (clicks * multiplier)
    supabase.table("saves").update({"cookies": new_cookies}).eq("id", save_id).execute()

    return jsonify({"cookies": new_cookies})


@game_api_bp.get("/api/saves")
def get_saves():
    if "user_id" not in session:
        return "Unauthorized", 401

    response = supabase.table("saves").select("*").eq("player_id", session["user_id"]).execute()
    return jsonify(response.data)


@game_api_bp.get("/api/saves/<save_id>")
def get_save(save_id):
    if "user_id" not in session:
        return "Unauthorized", 401

    response = supabase.table("saves").select("*").eq("id", save_id).eq("player_id", session["user_id"]).execute()
    if not response.data:
        return "Save not found", 404
    save = response.data[0]

    # Calculate offline progress
    response = supabase.table("inventory").select("*, items(*)").eq("save_id", save_id).execute()
    inventory = response.data
    auto_clicker_rate = 0
    for item in inventory:
        if item["items"]["effect"]["type"] == "auto_clicker":
            auto_clicker_rate += item["items"]["effect"]["value"] * item["quantity"]

    if auto_clicker_rate > 0:
        last_updated_at = datetime.fromisoformat(save["last_updated_at"])
        time_diff = datetime.now(timezone.utc) - last_updated_at
        cookies_generated = int(time_diff.total_seconds() * auto_clicker_rate)
        save["cookies"] += cookies_generated
        supabase.table("saves").update({
            "cookies": save["cookies"],
            "last_updated_at": datetime.now(timezone.utc).isoformat(),
        }).eq("id", save_id).execute()

    return jsonify(save)


@game_api_bp.post("/api/saves")
def create_save():
    if "user_id" not in session:
        return "Unauthorized", 401

    data = request.get_json()
    save_name = data["save_name"]

    supabase.table("saves").insert({
        "player_id": session["user_id"],
        "save_name": save_name,
    }).execute()

    return "Save created", 201


@game_api_bp.delete("/api/saves/<save_id>")
def delete_save(save_id):
    if "user_id" not in session:
        return "Unauthorized", 401

    supabase.table("saves").delete().eq("id", save_id).eq("player_id", session["user_id"]).execute()
    return "Save deleted", 200
