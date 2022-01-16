class HistoryService:

    def __init__(self, dao):
        self.dao = dao

    def record_login(self, user_id, login_time):
        return self.dao.record_login(user_id, login_time)
    
    def record_logout(self, user_id, login_time, logout_time):
        return self.dao.record_logout(user_id, login_time, logout_time)
