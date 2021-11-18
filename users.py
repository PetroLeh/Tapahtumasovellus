from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db

def login(username, password) -> bool:
    sql = "select id, password, is_admin FROM users WHERE username = :username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = username
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