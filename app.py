import os

from flask import Flask, redirect, render_template, session, url_for

from admin.routes import admin_bp
from auth.routes import auth_bp
from game_api.routes import game_api_bp

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")

app.register_blueprint(auth_bp)
app.register_blueprint(game_api_bp)
app.register_blueprint(admin_bp)


@app.get("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
