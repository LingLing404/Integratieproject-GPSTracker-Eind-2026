import os
from datetime import timedelta
from pathlib import Path

from flask import Flask, redirect, render_template, request, send_from_directory, session, url_for


BASE_DIR = Path(__file__).resolve().parent


def load_env_file():
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def required_env(name):
    value = os.environ.get(name)

    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value


load_env_file()

app = Flask(__name__, template_folder=".", static_folder=None)
app.secret_key = required_env("TRACKER_SESSION_SECRET")
app.permanent_session_lifetime = timedelta(days=30)

LOGIN_EMAIL = required_env("TRACKER_LOGIN_EMAIL")
LOGIN_PASSWORD = required_env("TRACKER_LOGIN_PASSWORD")


@app.get("/")
def index():
    return render_template("index.html", error=request.args.get("error"))


@app.post("/login")
def login():
    email = request.form.get("email", "")
    password = request.form.get("password", "")

    if email == LOGIN_EMAIL and password == LOGIN_PASSWORD:
        session.permanent = request.form.get("remember") == "on"
        session["user"] = email
        return redirect(url_for("dashboard"))

    return redirect(url_for("index", error="1"))


@app.get("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("index", error="login"))

    return render_template("dashboard.html")


@app.get("/styles.css")
def styles():
    return send_from_directory(".", "styles.css")


@app.get("/script.js")
def script():
    return send_from_directory(".", "script.js")


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
