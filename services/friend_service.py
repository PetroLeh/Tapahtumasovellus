class FriendService:

    def __init__(self, dao):
        self.dao = dao

    def get_friends(self, id) -> list:
        return self.dao.get_friends(id)

    def get_friend_invitations(self, id) -> list:
        return self.dao.get_friend_invitations(id)

    def is_friend(self, user1, user2) -> bool:
        return self.dao.is_friend(user1, user2)

    def add_friend(self, user1, user2) -> bool:
        if self.is_friend(user1, user2):
            return False
        return self.dao.add_friend(user1, user2)

    def add_friend_invitation(self, user1, user2) -> bool:
        return self.dao.add_friend_invitation(user1, user2)

    def has_friend_invitation(self, user1, user2) -> bool:
        return self.dao.has_friend_invitation(user1, user2)

    def remove_friend_invitation(self, user1, user2) -> bool:
        return self.dao.remove_friend_invitation(user1, user2)

    def invite_to_event(self, invited_by, friend_ids: list, event_id) -> bool:
        return self.dao.invite_to_event(invited_by, friend_ids, event_id)
    
    def who_are_invited_to_event(self, event_id, by_user):
        return self.dao.who_are_invited_to_event(event_id, by_user)