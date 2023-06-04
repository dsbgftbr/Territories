from flask import Flask, flash, redirect, request, render_template, session
from flask_session import Session


# Configure app
app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    if not session.get("username"):
        return redirect("/account/login")

    return render_template("index.html")


@app.route("/account/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Validate username and password
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        if not username or not password:
            flash("Invalid username or password")
            return redirect("/account/login")

        pass

    return render_template("login.html")
