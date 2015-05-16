from events.models import Event


class EventLogger:
    def __init__(self, action, response, request, additional=None, invoker=None):
        self.action = action
        self.response = response
        self.additional = additional

        self.request = request
        self.invoker = self.request.user.username

        self.log_event()

    def log_event(self):
        # Let's grab the current IP of the user.
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')

        Event(invoker=self.invoker, action=self.action, response=self.response, ip=ip,
              additional=self.additional).save()
