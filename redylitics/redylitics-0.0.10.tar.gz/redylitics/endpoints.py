#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, datetime

from redylitics.clients import PageviewClient, VideoClient, VideoAdClient
from redylitics.utils import LOGGER


pageview_client = PageviewClient()
video_client = VideoClient()
video_ad_client = VideoAdClient()


def update_channels(counter):
    """attempts to update a channel's pageview

    :param counter: the pageviews counter from the wsgi process
    :type counter: collections.Counter
    """
    t = date.today()
    today = datetime(t.year, t.month, t.day).strftime("%Y%m%d")
    for channel, incr in counter.items():
        channel = "{}{}".format(channel, today)
        try:
            output = pageview_client.update_channel(channel, incr)
            LOGGER.info("incr {} {}: {}".format(channel, incr, output))
        except Exception as e:
            LOGGER.exception(e)


def update_videos(counter):
    """attempts to update a video's event counts

    :param counter: the video counter from the wsgi process
    :type counter: collections.Counter
    """
    for (video, event), incr in counter.items():
        try:
            output = video_client.update_video(video, event, incr)
            LOGGER.info("hincr {} {} {}: {}".format(video, event, incr, output))
        except Exception as e:
            LOGGER.exception(e)


def update_video_ads(counter):
    """attempts to update a video ad's event counts

    :param counter: the video ad counter from the wsgi process
    :type counter: collections.Counter
    """
    for (video, event), incr in counter.items():
        try:
            output = video_ad_client.update_video(video, event, incr)
            LOGGER.info("hincr {} {} {}: {}".format(video, event, incr, output))
        except Exception as e:
            LOGGER.exception(e)


def read_channels(channel):
    """gets the dates and pageviews for a given channel + date string

    :param channel: the name of the channel + a date string
    :type channel: str

    :return: date: value key pairs and an is ok? value
    :rtype: dict, bool
    """
    try:
        res = pageview_client.read_channel(channel)
        return res, True
    except Exception as e:
        return str(e), False


def read_videos(video, event=None):
    """gets the counts for events for a given video

    :param video: the id of the video
    :type video: int

    :param event: the name of the event
    :type event: str

    :return: event: value key pairs and an is ok? value
    :rtype: dict, bool
    """
    try:
        video = int(video)
        res = video_client.read_video(video, event)
        return res, True
    except Exception as e:
        return str(e), False


def read_video_ads(ad, event=None):
    """gets the counts for events for a given video ad

    :param ad: the id of the video ad
    :type ad: int

    :param event: the name of the event
    :type event: str

    :return: event: value key pairs and an is ok? value
    :rtype: dict, bool
    """
    try:
        ad = int(ad)
        res = video_ad_client.read_video(ad, event)
        return res, True
    except Exception as e:
        return str(e), False
