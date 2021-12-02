
class Event:

    def __init__(self, user_id, created_at, start_time, end_time, description, info):
        self.user_id = user_id
        self.created_at = created_at
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.info = info

class EventService:

    def __init__(self, dao):
        self.dao = dao
        self.temp_event = None      # This variable is used for temporarily store an event
                                    # when handling attempts to add duplicate events
    def list_all(self):
        eventlist = self.dao.list_all()
        return eventlist

    def get_user(self, event_id):
        user_id = self.dao.get_user(event_id)
        return user_id

    def remove(self, id):
        self.dao.remove(id)

    def create(self, event):
        return self.dao.create(event)

    def get(self, id):
        return self.dao.get(id)

    def attendances(self, id):
        return self.dao.attendances(id)

    def duplicates(self, event):
        return self.dao.duplicates(event)
