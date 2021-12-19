from db import db

def send_message(user_id, message_to, message):
    try:
        sql = "INSERT INTO messages (user_from, user_to, message) VALUES (:user_id, :message_to, :message)"
        db.session.execute(sql, {"user_id": user_id,
                                 "message_to": message_to,
                                 "message": message})
        db.session.commit()
        return True
    except:
        return False

def sent(user_id):
    sql = "SELECT m.id, m.user_to AS receiver, m.message, u.username " \
          "FROM messages m, users u WHERE m.user_from=:user_id AND u.id=m.user_to"
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()

def received(user_id):
    sql = "SELECT m.id, m.user_from AS sender, m.message, u.username " \
          "FROM messages m, users u WHERE m.user_to=:user_id AND u.id=m.user_from"
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()
