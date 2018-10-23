class User:
    greeted = False
    received_inicial_message = False
    def __init__(self, user_id, first_name, last_name, username):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
