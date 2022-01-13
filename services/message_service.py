class MessageService:

    def __init__(self, dao):
        self.dao = dao

    def send_message(self, user_id, message_to, message):
        return self.dao.send_message(user_id, message_to, message)

    def sent(self, user_id):
        return self.dao.sent(user_id)
    
    def received(self, user_id):
        return self.dao.received(user_id)

    def new_messages(self, user_id):
        return self.dao.new_messages(user_id)

    def mark_all_as_read(self, user_id):
        return self.dao.mark_all_as_read(user_id)