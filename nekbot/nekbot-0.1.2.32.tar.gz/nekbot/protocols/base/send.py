from nekbot.utils.strings import long_message

__author__ = 'nekmo'


class Send(object):
    def send_message(self, body, notice=False):
        raise NotImplementedError("This protocol can't send messages.")

    def short_message(self, body):
        self.send_method(body, not long_message(body))

    def send_warning(self, body):
        self.send_method('Warning: %s' % body, not long_message(body))

    def send_error(self, body):
        self.send_method('Error: %s' % body, not long_message(body))

    @property
    def send_method(self):
        return self.send_message


class MessageSend(object):
    def reply(self, body, notice=False):
        raise NotImplementedError("This protocol can't reply messages.")

    @property
    def send_method(self):
        return self.reply

    short_reply = Send.short_message.__func__
    reply_warning = Send.send_warning.__func__
    reply_error = Send.send_error.__func__