class Users:
    users_dict = {}

    def __init__(self, u_id) -> None:
        self.u_id: int = u_id
        Users.add_user(u_id=u_id, user=self)
        self.commands: str = ""
        self.request_time: str = ""

    @staticmethod
    def get_user(u_id):
        if Users.users_dict.get(u_id) is None:
            new_user = Users(u_id)
            return new_user
        return Users.users_dict.get(u_id)

    @classmethod
    def add_user(cls, u_id, user):
        cls.users_dict[u_id] = user