from db import db

def record_login(user_id, login_time):
    try:
        sql = "INSERT INTO login_history (user_id, login_time) VALUES (:user_id, :login_time)"
        result = db.session.execute(sql, {"user_id": user_id,
                                          "login_time": login_time})
        db.session.commit()
        return True
    except:    
        return False

def record_logout(user_id, login_time, logout_time):
    try:
        sql = "UPDATE login_history SET logout_time=:logout_time WHERE login_time=:login_time AND user_id=:user_id"
        db.session.execute(sql, {"user_id": user_id,
                                 "login_time": login_time,
                                 "logout_time": logout_time})
        db.session.commit()
        return True
    except:
        return False

def get_records():
    sql = "SELECT h.user_id, u.username, h.login_time, h.logout_time FROM login_history h " \
          "LEFT JOIN users u ON h.user_id=u.id ORDER BY login_time DESC"
    result = db.session.execute(sql)
    return result.fetchall()