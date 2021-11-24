from app import app
from flask import render_template, redirect, request, flash
from datetime import date
import users, events


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
            return render_template("login.html", message="kirjautuminen ei onnistunut")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("register.html", passwords_dont_match=True)
        elif len(password1) < 5:
            return render_template("register.html", password_too_short=True)
        elif users.username_exists(username):
            return render_template("register.html", username_exists=username)
        if users.create(username, password1):
            return redirect("/")
        else:
            return render_template("index.html", eventlist=events.list(), message="Käyttäjätunnuksen luomisessa tapahtui odottamaton virhe")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/event", methods=["GET", "POST"])
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

@app.route("/event/<int:id>/remove")
def remove_event(id):
    if (users.logged_in() == events.get_user(id) or users.is_admin()):
        events.remove(id)
        return redirect("/")
    return redirect("/")

@app.route("/event/<int:id>")
def event(id):
    event = events.get(id)
    event.start_time = parse_time(event.start_time, "ei ilmoitettu")
    event.end_time = parse_time(event.end_time, "ei ilmoitettu")
    event.created_at = parse_time(event.created_at)

    return render_template("event.html",
                            id=id,
                            username=users.username(event.user_id),
                            event=event)

@app.route("/event/<int:id>/attend")
def attend_event(id):
    if users.attend_event(id):
        print("Jiihaa!")
        return redirect("/event/" + str(id))
    return redirect("/")

@app.route("/user/<int:id>")
def user(id):
    user_data = users.get_data(id)
    if user_data:
        return render_template("user.html", 
                                user=user_data)
    return redirect("/")

def parse_time(value, value2 = ""):
    if value:
        days = {"Monday": "Maanantai",
                "Tuesday": "Tiistai",
                "Wednesday": "Keskiviikko",
                "Thursday": "Torstai",
                "Friday": "Perjantai",
                "Saturday": "Lauantai",
                "Sunday": "Sunnuntai"}
        
        day = days[value.strftime("%A")]
        return day + value.strftime(" %d.%m.%Y  klo %H:%M")
    return value2