from db import db

def group_name(id):
    sql = "SELECT name FROM groups WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    name = result.fetchone()[0]
    return name

def members(id) -> tuple:
    sql = "SELECT m.user_id, u.username FROM members m, users u WHERE m.group_id=:id AND m.user_id = u.id"
    result = db.session.execute(sql, {"id":id})
    members = result.fetchall()
    return members

def get_groups_of_user(id):
    sql = "SELECT g.id, g.name FROM groups g, members m WHERE m.user_id=:id AND m.group_id=g.id"
    result = db.session.execute(sql, {"id":id})
    groups = result.fetchall()
    return groups
