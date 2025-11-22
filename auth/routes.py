from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database import supabase

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if the username already exists
        response = supabase.table("players").select("id").eq("username", username).execute()
        if response.data:
            return "Username already exists", 400

        # Hash the password and insert the new user
        hashed_password = generate_password_hash(password)
        supabase.table("players").insert({
            "username": username,
            "password": hashed_password,
        }).execute()

        return redirect(url_for("auth.login"))

    return render_template("signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Retrieve the user from the database
        response = supabase.table("players").select("*").eq("username", username).execute()
        if not response.data:
            return "Invalid username or password", 401

        user = response.data[0]
        if not check_password_hash(user["password"], password):
            return "Invalid username or password", 401

        # Store the user in the session
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["is_staff"] = user["is_staff"]

        return redirect(url_for("index"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
