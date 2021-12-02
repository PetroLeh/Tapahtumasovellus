
class GroupService:

    def __init__(self, dao):
        self.dao  = dao

    def group_name(self, id):
        return self.dao.group_name(id)

    def members(self, id):
        return self.dao.members(id)

    def get_groups_of_user(self, id):
        return self.dao.get_groups_of_user(id)
