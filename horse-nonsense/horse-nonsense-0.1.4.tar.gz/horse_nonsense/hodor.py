from horse.bridles.base import ListenerBridle


class Hodor(ListenerBridle):

    class Meta(ListenerBridle.Meta):
        regex = '[Hh]odor'
        display_name = "Hodor"
        display_icon = "http://i.imgur.com/ubRJXtm.png"

    def execute(self, user, channel, match, context):
        self.message(channel, 'Hodor')
