from app import app
from flask import render_template, redirect, request
import users
import events

@app.route("/")
def index():
        return render_template("index.html", eventlist=events.list())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":    
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

@app.route("/create/event", methods=["GET", "POST"])
def create_event():
    if request.method == "GET" and users.logged_in():
        return render_template("event_form.html")
    elif request.method == "POST" and users.logged_in():
        user_id = users.logged_in()
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        description = request.form["description"]
        info = request.form["info"]
        if (events.create(user_id, start_time, end_time, description, info)):
            return redirect("/")
        else:
            print("Tapahtuman lisäämisessä tapahtui virhe")
    return redirect("/")

@app.route("/remove/event/<int:id>")
def remove_event(id):
    if (users.logged_in() == events.get_user(id) or users.is_admin()):
        events.remove(id)
        return redirect("/")
    return redirect("/")