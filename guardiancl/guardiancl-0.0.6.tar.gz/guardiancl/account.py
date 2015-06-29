class Account:
    email = ""
    user_key = ""
    api_key = ""

    def __init__(self, email, user_key, api_key):
        self.email = email
        self.user_key = user_key
        self.api_key = api_key