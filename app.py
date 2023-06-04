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
    if not session.get("usersname"):
        return redirect("/account/login")

    return render_template("index.html")


@app.route("/account/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pass

    return render_template("login.html")