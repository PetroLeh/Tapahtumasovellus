from db import db

def send_message(user_id, message_to, message):
    try:
        sql = "INSERT INTO messages (created_at, user_from, user_to, message) VALUES (NOW(), :user_id, :message_to, :message)"
        db.session.execute(sql, {"user_id": user_id,
                                 "message_to": message_to,
                                 "message": message})
        db.session.commit()
        return True
    except:
        return False

def sent(user_id):
    sql = "SELECT m.id, m.created_at, m.user_to AS receiver, m.message, u.username " \
          "FROM messages m, users u WHERE m.user_from=:user_id AND u.id=m.user_to " \
          "ORDER BY m.created_at DESC"
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()

def received(user_id):
    sql = "SELECT m.id, m.created_at, m.user_from AS sender, m.message, m.read, u.username " \
          "FROM messages m, users u WHERE m.user_to=:user_id AND u.id=m.user_from " \
          "ORDER BY m.created_at DESC"
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()

def new_messages(user_id):
    sql = "SELECT m.id, m.created_at, m.user_from AS sender, m.message, m.read, u.username " \
          "FROM messages m, users u WHERE m.user_to=:user_id AND u.id=m.user_from AND m.read=false " \
          "ORDER BY m.created_at DESC"
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()

def mark_all_as_read(user_id):
    try:
        sql = "UPDATE messages SET read=true WHERE user_to=:user_id"
        db.session.execute(sql, {"user_id": user_id})
        db.session.commit()
        return True
    except:
        return False
