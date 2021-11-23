from db import db

class Event:
    def __init__(self, user_id, created_at, start_time, end_time, description, info):
        self.user_id = user_id
        self.created_at = created_at
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.info = info

def list():
    sql = "SELECT e.id AS id, COALESCE(e.description, 'ei kuvausta') AS description, e.start_time AS start_time, u.username AS username FROM events e, users u " \
        "WHERE e.user_id = u.id ORDER BY e.id"
    result = db.session.execute(sql)
    eventlist = result.fetchall()
    return eventlist

def get_user(id):
    sql = "SELECT user_id FROM events WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    user_id = result.fetchone()[0]
    return user_id

def remove(id):
    sql = "DELETE FROM events WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    db.session.commit()

def create(user_id, start_time, end_time, description, info):
    if description is None or description.strip() == "":
        description = "ei kuvausta"
    try:
        sql = "INSERT INTO events (user_id, created_at, start_time, end_time, description, info) " \
            "VALUES (:user_id, NOW(), NULLIF(:start_time, '')::TIMESTAMP , NULLIF(:end_time,'')::TIMESTAMP, :description, :info)"
        result = db.session.execute(sql,
                {"user_id":user_id,
                "start_time":start_time,
                "end_time":end_time,
                "description":description,
                "info":info})
        db.session.commit()
    except:
        return False
    return True

def get(id):
    sql = "SELECT user_id, created_at, start_time, end_time, description, info FROM events WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    data = result.fetchone()
    event = Event(data.user_id, data.created_at, data.start_time, data.end_time, data.description, data.info)
    return event

def attendances(id):
    sql = "SELECT u.id AS user_id, u.username AS username " \
        "FROM users u, attendances a WHERE u.id = a.user_id AND a.event_id=:event_id"
    result = db.session.execute(sql, {"event_id":id})
    attendances = result.fetchall()
    return attendances
