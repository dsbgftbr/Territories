from flask import Flask, flash, redirect, request, render_template, session
from flask_session import Session
from helpers import get_child
import json
import requests


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

        # Validate using SignIn API
        url = "https://netzwelt-devtest.azurewebsites.net/Account/SignIn"
        param = {"username": username, "password": password}

        response = requests.post(url, json=param)

        if response.status_code != 200:
            flash("Invalid username or password")
            return redirect("/account/login")

        session["username"] = username
        return redirect("/")

    # if GET /account/login
    return render_template("login.html")


@app.route("/account/logout")
def logout():
    session["username"] = None
    return redirect("/")


@app.route("/territories")
def get_territories():
    if not session.get("username"):
        return redirect("/account/login")

    # Get territories from API
    url = "https://netzwelt-devtest.azurewebsites.net/Territories/All"
    response = requests.get(url)

    if response.status_code != 200:
        return render_template("territories.html", places=[])

    # Nest data for territories.html
    data = json.loads(response.text)["data"]

    nested_data = []

    areas = [t for t in data if not t["parent"]]

    for area in areas:
        a = area.copy()
        a["children"] = get_child(area, data)
        nested_data.append(a)

    return render_template("territories.html", places=nested_data)
