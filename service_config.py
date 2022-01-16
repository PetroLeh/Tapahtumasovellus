from dao import event_db_dao, user_db_dao, friend_db_dao, message_db_dao, history_db_dao

from services.user_service import UserService
from services.friend_service import FriendService
from services.message_service import MessageService
from services.history_service import HistoryService
from services.event_service import EventService, Event

events = EventService(event_db_dao)
friends = FriendService(friend_db_dao)
messages = MessageService(message_db_dao)
history = HistoryService(history_db_dao)
users = UserService(user_db_dao, friends)
