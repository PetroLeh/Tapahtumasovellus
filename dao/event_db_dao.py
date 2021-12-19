from db import db

class Event:
    def __init__(self, user_id, created_at, start_time, end_time, description, info):
        self.user_id = user_id
        self.created_at = created_at
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.info = info

def list_events(order_by, event_filter):
    try:
        by_user = ""
        order_by = "e." + order_by
        if event_filter:
            by_user = "AND u.id="  + str(event_filter)
        sql = "SELECT e.id AS id, COALESCE(e.description, 'ei kuvausta') AS description, e.start_time AS start_time, u.username AS username FROM events e, users u " \
            "WHERE e.user_id = u.id " + by_user + " ORDER BY " + order_by + ", description"
        result = db.session.execute(sql)
        eventlist = result.fetchall()
        return eventlist, True
    except:
        return [], False

def get_user(id):
    sql = "SELECT user_id FROM events WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    user_id = result.fetchone()[0]
    return user_id

def remove(id):
    sql = "DELETE FROM events WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    db.session.commit()

def create(event):
    if not event:
        return False    
    if event.description is None or event.description.strip() == "":
        event.description = "ei kuvausta"
    try:
        sql = "INSERT INTO events (user_id, created_at, start_time, end_time, description, info) " \
            "VALUES (:user_id, NOW(), NULLIF(:start_time, '')::TIMESTAMP , NULLIF(:end_time, '')::TIMESTAMP, :description, :info) RETURNING id"
        result = db.session.execute(sql,
                {"user_id":event.user_id,
                "start_time":event.start_time,
                "end_time":event.end_time,
                "description":event.description,
                "info":event.info})
        db.session.commit()
        id = result.fetchone()[0]
        return id
    except:
        return False


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

def duplicates(event):

    # I had to do this with if - else, for now anyway. I tried NULLIF with different variations
    # on this but just didn't get it work on both cases, timestamps with null and not-null values.
    if event.start_time:
        sql = "SELECT * " \
            "FROM events WHERE user_id=:user_id AND LOWER(description)=:description AND " \
            "start_time=:start_time"
    else:
        sql = "SELECT * " \
            "FROM events WHERE user_id=:user_id AND LOWER(description)=:description AND " \
            "start_time IS NULL"    

    result = db.session.execute(sql, {"user_id":event.user_id,
                                      "start_time":event.start_time,
                                      "description":event.description.lower()})
    duplicates = result.fetchall()
    return duplicates

def invitations_to_user(id):
    sql = "SELECT i.event_id, e.description, i.invited_by, u.username AS invited_by_name " \
          "FROM invitations i INNER JOIN events e ON i.event_id=e.id " \
          "INNER JOIN users u ON i.invited_by=u.id WHERE i.user_id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchall()
