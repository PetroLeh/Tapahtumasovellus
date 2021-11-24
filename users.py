from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db
import groups, friends

def get_data(id):
    if logged_in():
        if id == logged_in() or is_admin():
            data = {"username": username(id),
                    "groups": groups.get_groups_of_user(id),
                    "friends": friends.get_friends(id),
                    "attendances": [],
                    "invitations": [],
                    "messages": [],
                    "rights_to_modify": True
                    }
        else:
            data = {"username": username(id),
                    "groups": groups.get_groups_of_user(id),
                    "friends": friends.get_friends(id)
                    }
        return data
    return null

def login(username, password) -> bool:
    sql = "select id, username, password, is_admin FROM users WHERE LOWER(username)=:username"
    result = db.session.execute(sql, {"username":username.lower()})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = user.username
        session["is_admin"] = user.is_admin
        return True
    return False

def create(username, password) -> bool:
    hash_value = generate_password_hash(password)
    try:        
        sql = "INSERT INTO users (username, password, is_admin) VALUES (:username, :password, FALSE)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    if session.get("user_id"):
        del session["is_admin"]
        del session["user_id"]
        del session["username"]

def logged_in() -> int:
    return session.get("user_id", 0)

def is_admin() -> bool:
    return session.get("is_admin")

def username(id):
    sql = "SELECT username FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    username = result.fetchone()[0]
    return username

def username_exists(username):
    sql = "SELECT id FROM users WHERE LOWER(username)=:username"
    result = db.session.execute(sql, {"username":username.lower()})
    return result.fetchone()

def user_id_exists(id):
    return True

def attend_event(event_id):
    if not logged_in():
        return False

    user_id = logged_in()

    if user_attending_to(user_id, event_id):
        return False
    try:
        sql = "INSERT INTO attendances (user_id, event_id) VALUES (:user_id, :event_id)"
        db.session.execute(sql, {"user_id":user_id, "event_id":event_id})
        db.session.commit()      
        return True
    except:
        return False

def user_attending_to(user_id, event_id):
    sql = "SELECT 1 FROM attendances WHERE user_id=:user_id AND event_id=:event_id"
    result = db.session.execute(sql, {"user_id":user_id, "event_id":event_id})    
    return result.fetchone()