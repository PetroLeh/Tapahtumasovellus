from werkzeug.security import check_password_hash, generate_password_hash
from flask import session

class UserService:

    def __init__(self, dao, friend_service, group_service):
        self.dao = dao
        self.friends = friend_service
        self.groups = group_service

    def get_data(self, id):
        if self.logged_in():
            if id == self.logged_in() or self.is_admin():
                data = {"id":id,
                        "username": self.dao.username(id),
                        "groups": self.groups.get_groups_of_user(id),
                        "friends": self.friends.get_friends(id),
                        "friend_invitations":self.friends.get_friend_invitations(id),
                        "attendances": [1, 3],
                        "invitations": [2, 4],
                        "messages": ["oumaigaad!", "omg!"],
                        "rights_to_modify": True
                        }
            else:
                data = {"id":id,
                        "username": self.dao.username(id),
                        "groups": self.groups.get_groups_of_user(id),
                        "friends": self.friends.get_friends(id)
                        }
            return data
        return null

    def login(self, username, password) -> bool:
        return self.dao.login(username, password)

    def create(self, username, password) -> bool:
        return self.dao.create(username, password)

    def logout(self):
        if session.get("user_id"):
            del session["is_admin"]
            del session["user_id"]
            del session["username"]

    def logged_in(self) -> int:
        return session.get("user_id", 0)

    def is_admin(self) -> bool:
        return session.get("is_admin")

    def username(self, id):
        return self.dao.username(id)

    def username_exists(self, username):
        return self.dao.username_exists(username)

    def user_id_exists(self, id):
        return self.dao.user_id_exists(id)

    def attend_event(self, event_id):
        if not self.logged_in():
            return
        user_id = self.logged_in()

        self.dao.attend_event(user_id, event_id)

    def user_attending_to(self, user_id, event_id):
        return self.dao.user_attending_to(user_id, event_id)