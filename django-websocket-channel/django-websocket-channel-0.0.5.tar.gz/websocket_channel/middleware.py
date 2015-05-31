#-*- coding: utf-8 -*-

class ChannelMiddleware(object):
    def process(self, request, channel, subscriber):
        subscriber.subscribe(channel)