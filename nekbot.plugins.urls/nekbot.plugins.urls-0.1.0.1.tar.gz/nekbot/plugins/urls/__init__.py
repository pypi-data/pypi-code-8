# coding=utf-8
import re
from nekbot.core import event
from nekbot.plugins.urls import urlinfo

__author__ = 'Nekmo'

from nekbot.core.commands import command

# @command
# def urls(msg):
#     return 'Hello world!'


def get_short_domain(url):
    domain = re.sub('(.+:(?://|))', '', url, 1)
    domain = domain.replace('www.', '', 1)
    return domain


@event('message.groupchat.public')
def get_url(protocol, msg):
    if msg.is_own or msg.historical:
        return
    urls = re.findall('(https?:(?://|)[^ ]+)', msg.body)
    if not urls:
        return
    data = urlinfo.urlinfo(urls[0])
    if not data.title:
        return
    body = u'⚓'
    if data.source_url:
        body += ' %s:' % (get_short_domain(data.source_url)).capitalize()
    body += ' %s' % data.title
    if data.authors:
        body += ' by %s' % ', '.join(data.authors)
    if getattr(data, 'extra', False):
        body += ' %s' %  data.extra
    msg.reply(body)
