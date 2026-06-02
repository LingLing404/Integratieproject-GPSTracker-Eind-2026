import os

from flask import Flask, redirect, render_template, request, session, url_for


app = Flask(__name__, template_folder=".", static_folder=".", static_url_path="")
app.secret_key = os.environ.get("TRACKER_SESSION_SECRET", "change-this-secret-key")

LOGIN_EMAIL = os.environ.get("TRACKER_LOGIN_EMAIL", "team@gpstracker.be")
LOGIN_PASSWORD = os.environ.get("TRACKER_LOGIN_PASSWORD", "test1234")


@app.get("/")
def index():
    return render_template("index.html", error=request.args.get("error"))


@app.post("/login")
def login():
    email = request.form.get("email", "")
    password = request.form.get("password", "")

    if email == LOGIN_EMAIL and password == LOGIN_PASSWORD:
        session["user"] = email
        return redirect(url_for("dashboard"))

    return redirect(url_for("index", error="1"))


@app.get("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("index", error="login"))

    return render_template("dashboard.html")


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
