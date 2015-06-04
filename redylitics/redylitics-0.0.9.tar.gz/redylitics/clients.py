#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import re
import os

import redis


REDYLITICS_PAGEVIEW_CLIENT_WRITE_CHANNEL_REGEX = os.environ.get("REDYLITICS_PAGEVIEW_CLIENT_WRITE_CHANNEL_REGEX", ".*")
REDYLITICS_PAGEVIEW_CLIENT_WRITE_DATE_REGEX = os.environ.get("REDYLITICS_PAGEVIEW_CLIENT_WRITE_DATE_REGEX", ".*")
REDYLITICS_PAGEVIEW_CLIENT_READ_CHANNEL_REGEX = os.environ.get("REDYLITICS_PAGEVIEW_CLIENT_READ_CHANNEL_REGEX", ".*")
REDYLITICS_PAGEVIEW_CLIENT_READ_DATE_REGEX = os.environ.get("REDYLITICS_PAGEVIEW_CLIENT_READ_DATE_REGEX", ".*")
REDYLITICS_PAGEVIEW_CLIENT_DATE_EXTRACTION_REGEX = os.environ.get("REDYLITICS_PAGEVIEW_CLIENT_DATE_EXTRACTION_REGEX", "\d{8}")

VIDEO_EVENT_REGEX = os.environ.get("REDYLITICS_VIDEO_EVENT_REGEX", ".*")

VIDEO_CLIENT_PREFIX = os.environ.get("REDYLITICS_VIDEO_CLIENT_PREFIX", "video")

VIDEO_AD_CLIENT_PREFIX = os.environ.get("REDYLITICS_VIDEO_AD_CLIENT_PREFIX", "video_ad")

REDIS_HOST = os.environ.get("REDYLITICS_REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDYLITICS_REDIS_PORT", 6379)
REDIS_DB = os.environ.get("REDYLITICS_REDIS_DB", 0)

REDIS_KWARGS = {
    "host": REDIS_HOST,
    "port": REDIS_PORT,
    "db": REDIS_DB,
}


class BaseRedisClient(object):
    """a thin wrapper around the `redis.StrictRedis` client
    """

    def __init__(self, **kwargs):
        """initializes the client object with a `.connection` attribute

        :param kwargs: keyword arguments for building a `redis.StrictRedis` client
        :type kwargs: dict
        """
        if len(kwargs):
            redis_kwargs = kwargs
        else:
            redis_kwargs = REDIS_KWARGS
        self.connection = redis.StrictRedis(**redis_kwargs)


class PageviewClient(BaseRedisClient):
    """extends the base `BaseRedisClient` object for working with pageview data
    """

    WRITE_CHANNEL_REGEX = re.compile(REDYLITICS_PAGEVIEW_CLIENT_WRITE_CHANNEL_REGEX)

    WRITE_DATE_REGEX = re.compile(REDYLITICS_PAGEVIEW_CLIENT_WRITE_DATE_REGEX)

    READ_CHANNEL_REGEX = re.compile(REDYLITICS_PAGEVIEW_CLIENT_READ_CHANNEL_REGEX)

    READ_DATE_REGEX = re.compile(REDYLITICS_PAGEVIEW_CLIENT_READ_DATE_REGEX)

    DATE_EXTRACTION_REGEX = re.compile(REDYLITICS_PAGEVIEW_CLIENT_DATE_EXTRACTION_REGEX)

    def update_channel(self, channel, increment_by):
        """increments a channel value if the channel name, date and increment value are valid

        :param channel: a channel name + date string
        :type channel: str

        :param increment_by: the value to increment by
        :type increment_by: int

        :return: was the operation was successful?
        :rtype: bool
        """
        channel_is_valid = self.WRITE_CHANNEL_REGEX.match(channel) is not None
        if not channel_is_valid:
            raise Exception("The channel name supplied is not valid: it must be a lowercase site name")

        increment_by_is_valid = isinstance(increment_by, int)
        if not increment_by_is_valid:
            raise Exception("The increment value is not valid: it must be an integer")

        try:
            date_string = re.findall(self.WRITE_DATE_REGEX, channel)[0]
        except (TypeError, AttributeError, IndexError):
            raise Exception("The date string supplied is not valid: it must be a valid `YYYYmmdd` string")

        date_is_valid = self.validate_date(date_string)
        if not date_is_valid:
            raise Exception("The date string supplied is not valid: it must be a valid `YYYYmmdd` string")

        return self.connection.incrby(channel, increment_by)

    def read_channel(self, channel):
        """gets the value for a given channel on either a specific date or wildcard date if both are valid

        :param channel: a channel name + date/wildcard string
        :type channel: str

        :return: the set of values requested
        :rtype: dict
        """
        channel_is_valid = self.READ_CHANNEL_REGEX.match(channel) is not None
        if not channel_is_valid:
            raise Exception("The channel name supplied is not valid: it must be a lowercase site name")

        try:
            date_string = re.findall(self.READ_DATE_REGEX, channel)[0]
        except (TypeError, AttributeError, IndexError):
            raise Exception("The date string supplied is not valid: it must be a valid `YYYYmmdd` or `YYYYmm*` string")

        date_is_valid = self.validate_date(date_string)
        if not date_is_valid:
            raise Exception("The date string supplied is not valid: it must be a valid `YYYYmmdd` or `YYYYmm*` string")

        keys = self.connection.keys(channel)
        values = self.connection.mget(keys)
        for index, value in enumerate(values):
            values[index] = int(value)
        dates = []
        for key in keys:
            matches = self.DATE_EXTRACTION_REGEX.findall(key)
            if len(matches):
                date = datetime.datetime.strptime(matches[0], "%Y%m%d").strftime("%Y-%m-%d")
                dates.append(date)
        return dict(zip(dates, values))

    @staticmethod
    def validate_date(date_string):
        """validates a date string as being either YYYYmmdd or YYYYmm*

        :param date_string: the date string to be validated
        :type date_string: str

        :return: is the date valid?
        :rtype: bool
        """
        try:
            _ = datetime.datetime.strptime(date_string, '%Y%m%d')
            return True
        except (TypeError, ValueError):
            try:
                _ = datetime.datetime.strptime(date_string, '%Y%m*')
                return True
            except (TypeError, ValueError):
                return False


class BaseVideoClient(BaseRedisClient):
    """extends the base `BaseRedisClient` object for working with video type data
    """

    PREFIX = ""

    EVENT_REGEX = re.compile(VIDEO_EVENT_REGEX)

    def update_video(self, video, event, increment_by):
        """updates a video event hash value if the video, event and value are valid

        :param video: the id of the video
        :type video: int

        :param event: the name of the event
        :type event: str

        :param increment_by: the value to increment by
        :type increment_by: int

        :return: was the operation was successful?
        :rtype: bool
        """
        video_is_valid = isinstance(video, int)
        if not video_is_valid:
            raise Exception("The video identifier supplied is not valid: it must be an integer")

        event_is_valid = self.EVENT_REGEX.match(event) is not None
        if not event_is_valid:
            raise Exception(
                "The event name supplied is not valid: it must be 'start', 'complete', 'firstQuartile', "
                "'midpoint', or 'thirdQuartile'")

        increment_by_is_valid = isinstance(increment_by, int)
        if not increment_by_is_valid:
            raise Exception("The increment value is not valid: it must be an integer")

        keyed_video = self.update_video_id(video)

        return self.connection.hincrby(keyed_video, event, increment_by)

    def read_video(self, video, event=None):
        """gets the value of a video and optionally limited to a hash key

        :param video: the id of the video
        :type video: int

        :param event: the name of the event (optional)
        :type event: str

        :return: a hash of event values
        :rtype: dict
        """
        video_is_valid = isinstance(video, int)
        if not video_is_valid:
            raise Exception("The video identifier supplied is not valid: it must be an integer")

        event_is_valid = event is None or self.EVENT_REGEX.match(event) is not None
        if not event_is_valid:
            raise Exception(
                "The event name supplied is not valid: it must be 'start', 'complete', 'firstQuartile', "
                "'midpoint', or 'thirdQuartile'")

        keyed_video = self.update_video_id(video)

        video_hash = self.connection.hgetall(keyed_video)
        for key, value in video_hash.items():
            video_hash[key] = int(value)
        if event:
            return {event: video_hash.get(event)}
        return video_hash

    def update_video_id(self, video):
        """adds the client type prefix the to the video id

        :param video: the id of the video
        :type video: int

        :return: the updated video id
        :rtype: str
        """
        return "{}.{}".format(self.PREFIX, video)


class VideoClient(BaseVideoClient):
    """
    a client specifically for videos
    """

    PREFIX = VIDEO_CLIENT_PREFIX


class VideoAdClient(BaseVideoClient):
    """
    a client specifically for video ads
    """

    PREFIX = VIDEO_AD_CLIENT_PREFIX
