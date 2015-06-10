#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, datetime
import re

from redylitics.clients import SentinelClient
from redylitics.config import *
from redylitics.utils import logger


# pageview stuff

write_channel_regex = re.compile(WRITE_CHANNEL_REGEX_PATTERN)
write_date_regex = re.compile(WRITE_DATE_REGEX_PATTERN)
read_channel_regex = re.compile(READ_CHANNEL_REGEX_PATTERN)
read_date_regex = re.compile(READ_DATE_REGEX_PATTERN)
date_extraction_regex = re.compile(DATE_EXTRACTION_REGEX_PATTERN)


# video stuff

video_prefix = VIDEO_PREFIX
video_id_regex = re.compile(VIDEO_ID_REGEX_PATTERN)
video_event_regex = re.compile(VIDEO_EVENT_REGEX_PATTERN)


# video ad stuff

video_ad_prefix = VIDEO_AD_PREFIX
video_ad_id_regex = re.compile(VIDEO_AD_ID_REGEX_PATTERN)
video_ad_event_regex = re.compile(VIDEO_AD_EVENT_REGEX_PATTERN)


def validate_date(date_string):
    """validates a date string as being either YYYYmmdd or YYYYmm*

    :param date_string: the date string to be validated
    :type date_string: str

    :return: is the date valid?
    :rtype: bool
    """
    try:
        _ = datetime.strptime(date_string, '%Y%m%d')
        return True
    except (TypeError, ValueError):
        try:
            _ = datetime.strptime(date_string, '%Y%m*')
            return True
        except (TypeError, ValueError):
            return False


def update_channels(counter):
    """attempts to update a channel's pageview

    :param counter: the pageviews counter from the wsgi process
    :type counter: collections.Counter
    """
    t = date.today()
    today = datetime(t.year, t.month, t.day).strftime("%Y%m%d")

    for channel, incr in counter.items():
        channel = "{}{}".format(channel, today)

        channel_is_valid = write_channel_regex.match(channel) is not None
        if not channel_is_valid:
            logger.error("bad channel. skipping. `{}`".format(channel))
            continue

        incr_is_valid = isinstance(incr, int)
        if not incr_is_valid:
            logger.error("bad increment value. skipping channel {}. `{}`".format(channel, incr))
            continue

        try:
            client = SentinelClient(SENTINEL_HOSTS, SENTINEL_PORT, SENTINEL_MASTER_NAME)
            output = client.set_one(channel, incr)
            logger.info("incr {} {}: {}".format(channel, incr, output))
        except Exception as e:
            logger.exception(e)


def update_videos(counter):
    """attempts to update a video's event counts

    :param counter: the video counter from the wsgi process
    :type counter: collections.Counter
    """
    for (video, event), incr in counter.items():
        video_is_valid = video_id_regex.match(video) is not None
        if not video_is_valid:
            logger.error("bad video id. skipping. `{}`".format(video))
            continue

        video = "{}.{}".format(video_prefix, video)

        event_is_valid = video_event_regex.match(event) is not None
        if not event_is_valid:
            logger.error("bad event. skipping video {}. `{}`".format(video, event))
            continue

        incr_is_valid = isinstance(incr, int)
        if not incr_is_valid:
            logger.error("bad increment value. skipping video.event {}.{}. `{}`".format(video, event, incr))
            continue

        try:
            client = SentinelClient(SENTINEL_HOSTS, SENTINEL_PORT, SENTINEL_MASTER_NAME)
            output = client.set_one_hash(video, event, incr)
            logger.info("hincr {} {} {}: {}".format(video, event, incr, output))
        except Exception as e:
            logger.exception(e)


def update_video_ads(counter):
    """attempts to update a video ad's event counts

    :param counter: the video ad counter from the wsgi process
    :type counter: collections.Counter
    """
    for (video, event), incr in counter.items():
        video_is_valid = video_ad_id_regex.match(video) is not None
        if not video_is_valid:
            logger.error("bad video ad id. skipping. `{}`".format(video))
            continue

        video = "{}.{}".format(video_ad_prefix, video)

        event_is_valid = video_ad_event_regex.match(event) is not None
        if not event_is_valid:
            logger.error("bad event. skipping video ad {}. `{}`".format(video, event))
            continue

        incr_is_valid = isinstance(incr, int)
        if not incr_is_valid:
            logger.error("bad increment value. skipping video_ad.event {}.{}. `{}`".format(video, event, incr))
            continue

        try:
            client = SentinelClient(SENTINEL_HOSTS, SENTINEL_PORT, SENTINEL_MASTER_NAME)
            output = client.set_one_hash(video, event, incr)
            logger.info("hincr {} {} {}: {}".format(video, event, incr, output))
        except Exception as e:
            logger.exception(e)


def read_channels(channel):
    """gets the dates and pageviews for a given channel + date string

    :param channel: the name of the channel + a date string
    :type channel: str

    :return: date: value key pairs and an is ok? value
    :rtype: dict, bool
    """
    channel_is_valid = read_channel_regex.match(channel) is not None
    if not channel_is_valid:
        return {"error": "The channel name supplied is not valid"}, False

    date_string = read_date_regex.findall(channel)
    if not len(date_string):
        return {"error": "Could not parse date attached to the channel: {}".format(read_date_regex.pattern)}, False
    date_string = date_string[0]

    date_is_valid = validate_date(date_string)
    if not date_is_valid:
        return {"error": "The date attached to the channel is not valid"}, False

    try:
        client = SentinelClient(SENTINEL_HOSTS, SENTINEL_PORT, SENTINEL_MASTER_NAME)
        result = client.get_many(channel)

        keys = [r[0] for r in result]
        values = [r[1] for r in result]

        for index, value in enumerate(values):
            values[index] = int(value)

        dates = []
        for key in keys:
            matches = date_extraction_regex.findall(key)
            if len(matches):
                date_key = datetime.strptime(matches[0], "%Y%m%d").strftime("%Y-%m-%d")
                dates.append(date_key)

        return dict(zip(dates, values)), True

    except Exception as e:
        return str(e), False


def read_videos(video, event=None):
    """gets the counts for events for a given video

    :param video: the id of the video
    :type video: str

    :param event: the name of the event
    :type event: str

    :return: event: value key pairs and an is ok? value
    :rtype: dict, bool
    """
    video_is_valid = video_id_regex.match(video) is not None
    if not video_is_valid:
        return {"error": "The video id supplied is not valid"}, False

    video = "{}.{}".format(video_prefix, video)

    if event:
        event_is_valid = video_event_regex.match(event) is not None
        if not event_is_valid:
            return {"error": "The event name supplied is not valid"}, False
        event = [event, ]

    try:
        client = SentinelClient(SENTINEL_HOSTS, SENTINEL_PORT, SENTINEL_MASTER_NAME)
        result = client.get_one_hash(video, event)
        return result, True
    except Exception as e:
        return str(e), False


def read_video_ads(ad, event=None):
    """gets the counts for events for a given video ad

    :param ad: the id of the video ad
    :type ad: str

    :param event: the name of the event
    :type event: str

    :return: event: value key pairs and an is ok? value
    :rtype: dict, bool
    """
    video_is_valid = video_id_regex.match(ad) is not None
    if not video_is_valid:
        return {"error": "The video id supplied is not valid"}, False

    video = "{}.{}".format(video_ad_prefix, ad)

    if event:
        event_is_valid = video_event_regex.match(event) is not None
        if not event_is_valid:
            return {"error": "The event name supplied is not valid"}, False
        event = [event, ]

    try:
        client = SentinelClient(SENTINEL_HOSTS, SENTINEL_PORT, SENTINEL_MASTER_NAME)
        result = client.get_one_hash(video, event)
        return result, True
    except Exception as e:
        return str(e), False
