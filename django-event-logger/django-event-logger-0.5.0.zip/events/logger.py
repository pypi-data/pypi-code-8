from events.models import Event


class Events:
    def __init__(self):
        pass

    def log_event(self, username, action, response, additional='N/A'):
        try:
            log = Event(username=username, action=action, response=response, additional=additional)
            log.save()
        except:
            raise Exception