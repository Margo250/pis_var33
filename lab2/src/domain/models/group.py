class Group:
    def __init__(self, group_id: str, name: str):
        self.id = group_id
        self.name = name
        self.member_ids = []
    
    def add_member(self, user_id: str):
        if user_id not in self.member_ids:
            self.member_ids.append(user_id)
