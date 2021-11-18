from db import db

def list():
    sql = "SELECT e.description AS description, e.start_time AS start_time, u.username AS username FROM events e, users u " \
        "WHERE e.user_id = u.id ORDER BY e.id"
    result = db.session.execute(sql)
    eventlist = result.fetchall()
    return eventlist