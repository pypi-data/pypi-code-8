from horse.bridles.base import EventBridle


class JoinNewChannel(EventBridle):

    class Meta(EventBridle.Meta):
        event = 'channel_created'

    def execute(self, data):
        self.jockey.slack.join_channel(data['channel'].name)


class JoinUnarchivedChannel(JoinNewChannel):

    class Meta(JoinNewChannel.Meta):
        event = 'channel_unarchive'


class JoinUnarchivedGroup(JoinNewChannel):

    class Meta(JoinNewChannel.Meta):
        event = 'group_unarchive'
