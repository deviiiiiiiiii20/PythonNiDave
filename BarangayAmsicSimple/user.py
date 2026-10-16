


class User:
    def __init__(self, user_id, full_name, username, role):
        self.user_id = user_id
        self.full_name = full_name
        self.username = username
        self.role = role

    def __str__(self):
        return self.full_name + " (" + self.role + ")"

    def __repr__(self):
        return f"User({self.user_id}, {self.username})"

    def __eq__(self, other):
        return self.user_id == other.user_id


class Resident(User):
    def __init__(self, user_id, full_name, username, address):
        super().__init__(user_id, full_name, username, "resident")
        self.address = address


class Staff(User):
    def __init__(self, user_id, full_name, username, position):
        super().__init__(user_id, full_name, username, "staff")
        self.position = position
