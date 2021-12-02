class FriendService:

    def __init__(self, dao):
        self.dao = dao

    def get_friends(self, id):
        return self.dao.get_friends(id)

    def get_friend_invitations(self, id):
        return self.dao.get_friend_invitations(id)

    def is_friend(self, user1, user2):
        return self.dao.is_friend(user1, user2)

    def add_friend(self, user1, user2):
        if self.is_friend(user1, user2):
            return False
        return self.dao.add_friend(user1, user2)
