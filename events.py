from db import db

class Event:
    def __init__(self, user_id, start_time, end_time, description, info):
        self.user_id = user_id
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.info = info

def list():
    sql = "SELECT e.id AS id, e.description AS description, e.start_time AS start_time, u.username AS username FROM events e, users u " \
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
    sql = "INSERT INTO events (user_id, start_time, end_time, description, info) " \
        "VALUES (:user_id, NULLIF(:start_time, '')::TIMESTAMP , NULLIF(:end_time,'')::TIMESTAMP, :description, :info)"
    result = db.session.execute(sql,
            {"user_id":user_id,
            "start_time":start_time,
            "end_time":end_time,
            "description":description,
            "info":info})
    db.session.commit()

def get(id):
    sql = "SELECT user_id, start_time, end_time, description, info FROM events WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    data = result.fetchone()
    event = Event(data.user_id, data.start_time, data.end_time, data.description, data.info)
    return event