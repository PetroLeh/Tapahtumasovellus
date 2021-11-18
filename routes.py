from app import app
from flask import render_template, redirect, request
import users

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if users.login(username, password):
        return redirect("/")
    else:
        return "kirjautuminen ei onnistunut"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return "salasanat olivat erit"
        if users.create(username, password1):
            return redirect("/")
        else:
            return "rekisteröinti ei onnistunut"

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")