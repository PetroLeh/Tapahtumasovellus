
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

    def list_events(self, order_by, event_filter=None):
        return self.dao.list_events(order_by, event_filter)

    def get_user(self, event_id):
        return self.dao.get_user(event_id)

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

    def invitations_to_user(self, id):
        return self.dao.invitations_to_user(id)
