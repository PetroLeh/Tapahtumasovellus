from flask import render_template, redirect, request, session, abort
from app import app

from service_config import Event, events, users, friends, messages, history

from datetime import datetime, timezone

########        Some help functions

def empty_event(description:str, info:str) -> bool:
    if description is not None and description.strip() != "" or info is not None and info.strip() != "":
        return False
    return True

def if_empty(attr1: str, attr2:str) -> str:
    if not attr1 or attr1.strip() == "":
        return attr2
    return attr1

def validate_times(start_time, end_time):
    now = datetime.now()
    st = now
    message = ""
    if start_time:
        st = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
        if st < now:
            st = now            
            message = "Alkuaika oli menneisyydessä, asetettiin tähän hetkeen. "
            start_time = datetime.strftime(st, "%Y-%m-%dT%H:%M")
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

def record_login_history(login_or_logout: str):
    if login_or_logout == "login":
        login_time_str = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        login_time = datetime.strptime(login_time_str, "%Y-%m-%d %H:%M:%S")
        session["login_time"] = login_time_str
        history.record_login(logged_in(), login_time) 
        return
    elif login_or_logout == "logout":
        login_time = datetime.strptime(session["login_time"], "%Y-%m-%d %H:%M:%S")
        logout_time_str = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        logout_time = datetime.strptime(logout_time_str, "%Y-%m-%d %H:%M:%S")
        history.record_logout(logged_in(), login_time, logout_time)
        return
    raise ValueError(f"Record_login_history should get 'login' or 'logout' as an attribute.\n'{login_or_logout}' is not a valid attribute.")

########        routes:

########        main page
@app.route("/")
def index():
    if logged_in():
        eventlist, query_successfull = events.list_events(order_by=session["event_sorter"], event_filter=session["event_filter"])
        new_messages = len(messages.new_messages(logged_in()))
        session["new_messages"] = new_messages
    else:
        eventlist, query_successfull = events.list_events(order_by="created_at DESC", event_filter=None)
    
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
            record_login_history("login")
            return redirect("/")
        return render_template("login.html",
                            message="kirjautuminen ei onnistunut")
    return redirect("/")

@app.route("/logout")
def logout():
    if logged_in():
        record_login_history("logout")
        users.logout()
    return redirect("/")

########        users
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

@app.route("/users")
def all_users():
    if not logged_in():
        return redirect("/")
    return render_template("users.html", all_users=users.get_all(logged_in()))

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
        description = request.form["description"]
        info = request.form["info"]
        if empty_event(description, info):
            return render_template("error.html",
                                   message="tapahtumaa ei lisätty, koska siitä ei annettu mitään tietoja")
        description = if_empty(description, "(ei kuvausta)")
        info = if_empty(info, f"(ei lisätietoja tapahtumasta '{description}')")

        event = Event(users.logged_in(),
                      None,          # 'event.created_at' is set to None here.
                      start_time,    # Correct timestamp will be set in
                      end_time,      # create() method in event_db_dao.
                      description,
                      info)
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
    friends_attending = friends.who_are_attending_to_event(id, logged_in())
    attendances = events.all_attendances_to_event(id)
    print(attendances)
    
    return render_template("event.html",
                           id=id,
                           username=users.username(event.user_id),
                           event=event,
                           attendances=attendances,
                           is_attending=users.user_attending_to(logged_in(), id),
                           friends=friends.get_friends(logged_in()),
                           friends_invited=friends_invited,
                           friends_attending=friends_attending)

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

@app.route("/event/invitation/remove/<int:id>")
def remove_invitation(id):
    if logged_in():
        events.remove_invitation(id)
        return redirect("/user/" + str(logged_in()))
    return redirect("/")

@app.route("/sort_method/<string:sorter>")
def sort_method(sorter):
    session["event_sorter"] = sorter
    return redirect("/")

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
                               event_invitations=events.invitations_to_user(id),
                               attended_events=events.all_events_user_is_attending(id),
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
                return redirect("/user/" + str(logged_in()))
    return redirect("/")

########        messages
@app.route("/messages", methods=["GET", "POST"])
def message():
    if request.method == "GET" and logged_in():
        messages_sent = messages.sent(logged_in())
        messages_received = messages.received(logged_in())
        if not messages_sent:
            messages_sent = []
        if not messages_received:
            messages_received = []

        if messages.new_messages(logged_in()):
            messages.mark_all_as_read(logged_in())
            del session["new_messages"]

        return render_template("messages.html",
                               friends=friends.get_friends(logged_in()),
                               messages_sent=messages_sent,
                               messages_received=messages_received)
    if request.method == "POST" and logged_in():
        try:
            receiver = request.form["receiver"]
            content = request.form["content"]
        except:
            return render_template("error.html",
                                   message="viestin lähettämisessä tapahtui virhe: Viestillä ei ole vastaanottajaa tai sisältöä.")            
        if not messages.send_message(logged_in(), receiver, content):
            return render_template("error.html",
                                   message="viestin lähettämisessä tapahtui virhe")
        return redirect("/messages")
    return redirect("/")

