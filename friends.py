from db import db

def get_friends(id):
    sql = "SELECT f.user2 AS id, u.username AS username " \
        "FROM friends f, users u WHERE f.user1=:id AND u.id = f.user2"
    result = db.session.execute(sql, {"id":id})
    friends = result.fetchall()
    return friends