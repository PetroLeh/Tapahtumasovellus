from repositories import event_db_dao, user_db_dao, friend_db_dao, group_db_dao

from services.user_service import UserService
from services.friend_service import FriendService
from services.group_service import GroupService
from services.event_service import EventService, Event

events = EventService(event_db_dao)
friends = FriendService(friend_db_dao)
groups = GroupService(group_db_dao)

users = UserService(user_db_dao, friends, groups)