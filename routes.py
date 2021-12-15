from flask import render_template, redirect, request
from app import app

from service_config import Event, events, users, friends, groups

def parse_time(value, value2=""):
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

def logged_in():
    return users.logged_in()

########        routes:

########        main page
@app.route("/")
def index():
    return render_template("index.html", eventlist=events.list_all())

########        login/logout
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        return render_template("login.html", message="kirjautuminen ei onnistunut")
    return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


########        register new user
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("register.html", passwords_dont_match=True)
        if len(password1) < 5:
            return render_template("register.html", password_too_short=True)
        if users.username_exists(username):
            return render_template("register.html", username_exists=username)
        if users.create(username, password1):
            return redirect("/")
        else:
            return render_template("error.html",
                                   message="Käyttäjätunnuksen luomisessa tapahtui odottamaton virhe")
    return redirect("/")

########        events
@app.route("/event", methods=["GET", "POST"])
def create_event():
    if request.method == "GET" and logged_in():
        return render_template("event_form.html")
    if request.method == "POST" and logged_in():
        event = Event(users.logged_in(),
                      None,                          # 'event.created_at' is set to None here.
                      request.form["start_time"],    # Correct timestamp will be set in
                      request.form["end_time"],      # create() method in event_db_dao.
                      request.form["description"],
                      request.form["info"])
        duplicates = events.duplicates(event)
        if duplicates:
            events.temp_event = event
            return render_template("event_form.html",
                                   count=len(duplicates),
                                   duplicates=duplicates,
                                   event=event,
                                   start_time=parse_time(duplicates[0].start_time, "ei ilmoitettu"))
        if not events.create(event):
            return render_template("error.html", message="virhe tapahtuman lisäämisessä")
    return redirect("/")

@app.route("/event/duplicate")
def handle_duplicate():
    if not events.create(events.temp_event):
        events.temp_event = None
        return render_template("error.html", message="virhe tapahtuman lisäämisessä")
    events.temp_event = None
    return redirect("/")

@app.route("/event/<int:id>/remove")
def remove_event(id):
    if (logged_in() == events.get_user(id) or users.is_admin()):
        events.remove(id)
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
                           event=event,
                           is_attending=users.user_attending_to(logged_in(), id))

@app.route("/event/<int:id>/attend")
def attend_event(id):
    users.attend_event(id)
    return redirect("/event/" + str(id))


########        users personal page
@app.route("/user/<int:id>")
def user(id):
    if not users.user_id_exists(id):
        return redirect("/")
    user_data = users.get_data(id)
    if user_data:
        return render_template("user.html",
                               user=user_data,
                               friend=friends.is_friend(logged_in(), id))
    return redirect("/")

########        friends
@app.route("/friends")
def friends_page():
    if logged_in():
        return render_template("friends.html")
    return redirect("/")

@app.route("/friends/add/<int:id>")
def add_friend(id):
    if logged_in():
        if friends.add_friend(logged_in(), id):
            return redirect("/user/" + str(id))
        return render_template("error.html", message="Virhe ystävän lisäämisessä")
    return redirect("/")

########    groups
@app.route("/groups")
def groups():
    if logged_in():
        return render_template("groups.html")
    return redirect("/")
