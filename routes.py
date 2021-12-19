from flask import render_template, redirect, request, session, abort
from app import app

from service_config import Event, events, users, friends, groups

from datetime import datetime

########        Some help functions

def validate_times(start_time, end_time):
    now = datetime.now()
    st = now
    message = ""
    if start_time:
        st = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
        if st < now:
            print("alkuaika oli", start_time, "| st:", st, "| now:", now)
            st = now            
            message = "Alkuaika oli menneisyydessä, asetettiin tähän hetkeen. "
            start_time = datetime.strftime(st, "%Y-%m-%dT%H:%M")
            print("uusi alkuaika:", start_time)
    if end_time:
        et = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
        if et < st:
            end_time = ""
            message = message + "Lopetusajaksi muutettiin 'ei ilmoitettu' sillä se oli asetettu aikaisemmaksi kuin aloitusaika tai nykyhetki."

    return start_time, end_time, message

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

def map_list_to_int(list_to_map):
    return [int(item) for item in list_to_map]

def get_ids(user_list):
    res = []
    for user in user_list:
        res.append(user.id)
    return res

def remove_from_list(original_list, to_remove: list):
    res = []
    for item in original_list:
        if item not in to_remove:
            res.append(item)
    return res

def logged_in():
    return users.logged_in()

########        routes:

########        main page
@app.route("/")
def index():
    if logged_in():
        eventlist, query_successfull = events.list_events(order_by=session["event_sorter"], event_filter=session["event_filter"])
    else:
        eventlist, query_successfull = events.list_events(order_by="start_time", event_filter=None)
    if query_successfull:
        return render_template("index.html", eventlist=eventlist)
    return render_template("error.html",
                           message="Virhe tapahtumien lataamisessa")

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
        return render_template("login.html",
                            message="kirjautuminen ei onnistunut")
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
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        start_time, end_time, message = validate_times(request.form["start_time"],
                                                       request.form["end_time"])
        event = Event(users.logged_in(),
                      None,          # 'event.created_at' is set to None here.
                      start_time,    # Correct timestamp will be set in
                      end_time,      # create() method in event_db_dao.
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
        event_id = events.create(event)
        if not event_id:
            return render_template("error.html", message="virhe tapahtuman lisäämisessä")
        if message:
            eventlist, query_successfull = events.list_events(order_by=session["event_sorter"], event_filter=session["event_filter"])
            return render_template("index.html",
                                   eventlist=eventlist,
                                   message=message)      
        return redirect("/event/" + str(event_id))
    return redirect("/")

@app.route("/event/duplicate")
def handle_duplicate():
    event_id = events.create(events.temp_event)
    if not event_id:
        events.temp_event = None
        return render_template("error.html", message="virhe tapahtuman lisäämisessä")
    events.temp_event = None
    return redirect("/event/" + str(event_id))

@app.route("/event/<int:id>/remove", methods=["POST"])
def remove_event(id):
    if (logged_in() == events.get_user(id) or users.is_admin()):
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        events.remove(id)
    return redirect("/")

@app.route("/event/<int:id>")
def event(id):
    event = events.get(id)
    event.start_time = parse_time(event.start_time, "ei ilmoitettu")
    event.end_time = parse_time(event.end_time, "ei ilmoitettu")
    event.created_at = parse_time(event.created_at)

    friends_invited = friends.who_are_invited_to_event(id, logged_in())
    return render_template("event.html",
                           id=id,
                           username=users.username(event.user_id),
                           event=event,
                           is_attending=users.user_attending_to(logged_in(), id),
                           friends=friends.get_friends(logged_in()),
                           friends_invited=friends_invited)

@app.route("/event/<int:id>/attend")
def attend_event(id):
    users.attend_event(id)
    return redirect("/event/" + str(id))

@app.route("/event/<int:id>/invite", methods=["POST"])
def invite_to_event(id):
    if logged_in():
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        friends_to_invite = map_list_to_int(request.form.getlist("friend"))
        friends_to_invite = remove_from_list(friends_to_invite, get_ids(friends.who_are_invited_to_event(id, logged_in())))
        friends.invite_to_event(logged_in(), friends_to_invite, id)
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
                               friend=friends.is_friend(logged_in(), id),
                               has_friend_invitation=friends.has_friend_invitation(logged_in(), id),
                               has_invited_as_a_friend=friends.has_friend_invitation(id, logged_in()),
                               event_invitations=events.invitations_to_user(logged_in()),
                               all_users=users.get_all(logged_in()))                        
    return redirect("/")

########        friends
@app.route("/friends")
def friends_page():
    if logged_in():
        return render_template("friends.html")
    return redirect("/")

@app.route("/friends/send_friend_invitation/<int:id>")
def send_friend_invitation(id):
    if logged_in():
        if not friends.has_friend_invitation(logged_in(), id) and not friends.has_friend_invitation(id, logged_in()):
            if friends.add_friend_invitation(logged_in(), id):
                return redirect("/user/" + str(id))
            return render_template("error.html", message="Virhe ystäväkutsun lähettämisessä")
    return redirect("/")

@app.route("/friends/add/<int:id>")
def add_friend(id):
    if logged_in():
        if not friends.is_friend(logged_in(), id):
            if friends.has_friend_invitation(id, logged_in()):
                if friends.add_friend(logged_in(), id):
                    friends.remove_friend_invitation(id, logged_in())                
                return redirect("/user/" + str(id))
    return redirect("/")

########    groups
@app.route("/groups")
def groups():
    if logged_in():
        return render_template("groups.html")
    return redirect("/")
