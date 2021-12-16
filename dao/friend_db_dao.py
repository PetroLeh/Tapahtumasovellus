from db import db

def get_friends(id):
    sql = "SELECT f.user2 AS id, u.username AS username " \
        "FROM friends f, users u WHERE f.user1=:id AND f.user2=u.id ORDER BY username"
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
    
def has_friend_invitation(user1, user2):
    sql = "SELECT 1 FROM friend_invitations WHERE user1=:user1 AND user2=:user2"
    result = db.session.execute(sql, {"user1": user1, "user2": user2})
    return result.fetchone()

def add_friend_invitation(user1, user2):
    try:
        sql = "INSERT INTO friend_invitations (user1, user2) VALUES (:user1, :user2)"
        db.session.execute(sql, {"user1": user1, "user2": user2})
        db.session.commit()
        return True
    except:
        return False

def remove_friend_invitation(user1, user2):
    try:
        sql = "DELETE FROM friend_invitations WHERE user1=:user1 AND user2=:user2"
        db.session.execute(sql, {"user1": user1, "user2": user2})
        db.session.commit()
        return True
    except:
        return False

def invite_to_event(invited_by, friends_invited, event_id):
    try:
        sql = """INSERT INTO invitations (user_id, invited_by, event_id)
                 SELECT i, :invited_by, :event_id
                 FROM unnest(:friends_invited) i"""
        db.session.execute(sql, {"friends_invited": friends_invited,
                                 "invited_by": invited_by,
                                 "event_id": event_id})
        db.session.commit()
        return True
    except:
        return False

def who_are_invited_to_event(event_id, by_user):
    sql = "SELECT u.id, u.username FROM invitations i, users u " \
        "WHERE i.user_id=u.id AND i.event_id=:event_id AND i.invited_by=:by_user"
    result = db.session.execute(sql, {"event_id": event_id,
                                      "by_user": by_user})
    return result.fetchall()