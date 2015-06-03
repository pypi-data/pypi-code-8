import re
import six


class BridleBase(type):

    class DefaultMeta(object):
        pass

    def __new__(cls, name, bases, attrs):
        meta = attrs.pop('Meta', None)
        new_class = super(BridleBase, cls).__new__(cls, name, bases, attrs)
        if meta is None:
            meta = BridleBase.DefaultMeta
        if 'abstract' not in meta.__dict__:
            meta.abstract = False
        new_class.Meta = meta
        return new_class


class Bridle(six.with_metaclass(BridleBase)):

    class Meta:
        abstract = True
        display_name = 'Horse'
        display_icon = 'http://ryangrieve.com/labs/slack_icons/horse.png'
        description = 'No description provided'

    def __init__(self, jockey):
        self.jockey = jockey

    def message(self, channel, message, **kwargs):
        if 'username' not in kwargs:
            kwargs['username'] = self.Meta.display_name
        if 'icon_url' not in kwargs:
            kwargs['icon_url'] = self.Meta.display_icon

        self.jockey.slack.send_message(
            channel=channel,
            text=message,
            **kwargs
        )


class CommandBridle(Bridle):

    class Meta(Bridle.Meta):
        abstract = True
        command = ''
        help_text = ['No help text provided']
        secret = False

    def execute(self, user, channel, operands):
        return ""


class ListenerBridle(Bridle):

    class Meta(Bridle.Meta):
        abstract = True
        regex = ''

    def __init__(self, jockey):
        super(ListenerBridle, self).__init__(jockey)
        self._pattern = re.compile(self.Meta.regex)

    def execute(self, user, channel, context):
        return ""


class WebhookBridle(Bridle):

    class Meta(Bridle.Meta):
        abstract = True
        method = 'GET'
        path = ''

    def execute(self, path, data):
        return ""


class EventBridle(Bridle):

    class Meta(Bridle.Meta):
        abstract = True
        event = ''

    def execute(self, data):
        return ""
