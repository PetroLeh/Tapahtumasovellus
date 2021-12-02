class FriendService:

    def __init__(self, dao):
        self.dao = dao

    def get_friends(self, id):
        return self.dao.get_friends(id)