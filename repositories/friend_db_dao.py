from db import db

def get_friends(id):
    sql = "SELECT f.user2 AS id, u.username AS username " \
        "FROM friends f, users u WHERE f.user1=:id AND u.id = f.user2"
    result = db.session.execute(sql, {"id":id})
    friends = result.fetchall()
    return friends

def get_friend_invitations(id):
    sql = "SELECT f.user1 AS id, u.username AS username FROM friend_invitations f, " \
        "users u WHERE f.user1=u.id AND f.user2=:id"
    result = db.session.execute(sql, {"id":id})
    invitations = result.fetchall()
    return invitations

def is_friend(user1, user2):
    sql = "SELECT 1 FROM friends WHERE user1=:user1 AND user2=:user2"
    result = db.session.execute(sql, {"user1":user1, "user2":user2})
    return result.fetchone()

def add_friend(user1, user2):
    try:
        sql = "INSERT INTO friends (user1, user2) VALUES (:user1, :user2), (:user2, :user1)"
        result = db.session.execute(sql, {"user1":user1, "user2":user2})
        db.session.commit()
        return True
    except: 
        return False