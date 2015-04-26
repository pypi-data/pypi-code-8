from datetime import datetime


class Message(object):
    
    def __init__(self, data, conversation):
        self.data = data
        self.conversation = conversation

    def get_sender(self):
        """
        Returns string representing sender name
        """
        return self.data["from"]["name"]

    def get_message(self):
        return self.data.get("message", "")

    def __str__(self):
        return self.get_message()

    def get_time(self):
        return datetime.strptime(self.data["created_time"], "%Y-%m-%dT%H:%M:%S%z")
