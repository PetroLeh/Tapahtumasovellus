from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db

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
    sql = "SELECT 1 FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def attend_event(user_id, event_id):
    if user_attending_to(user_id, event_id):
        sql = "DELETE FROM attendances WHERE user_id=:user_id AND event_id=:event_id"
        db.session.execute(sql, {"user_id":user_id, "event_id":event_id})
        db.session.commit()   
    else:
        sql = "INSERT INTO attendances (user_id, event_id) VALUES (:user_id, :event_id)"
        db.session.execute(sql, {"user_id":user_id, "event_id":event_id})
        db.session.commit()

def user_attending_to(user_id, event_id):
    if not user_id or not event_id:
        return False
    sql = "SELECT 1 FROM attendances WHERE user_id=:user_id AND event_id=:event_id"
    result = db.session.execute(sql, {"user_id":user_id, "event_id":event_id})    
    return result.fetchone()