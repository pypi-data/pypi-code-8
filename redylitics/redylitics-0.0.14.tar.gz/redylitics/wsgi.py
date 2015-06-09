#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
import json
import re

import gevent
from gevent import queue

from redylitics.config import FLUSH_INTERVAL, REFERER_EXTRACT_REGEX_PATTERN, REFERER_ANCHORED_REGEX_PATTERN
from redylitics.endpoints import update_channels, update_video_ads, update_videos, \
    read_channels, read_videos, read_video_ads
from redylitics.utils import logger, gif

try:
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import parse_qs


# init the gevent queue
channel_queue = queue.Queue()
video_queue = queue.Queue()
video_ad_queue = queue.Queue()
flush_interval = FLUSH_INTERVAL

# endpoint regexes
referer_extract_regex = re.compile(REFERER_EXTRACT_REGEX_PATTERN)
referer_anchored_regex = re.compile(REFERER_ANCHORED_REGEX_PATTERN)


# get http referer
def get_referer(env):
    try:
        ref = env["HTTP_REFERER"]
    except KeyError:
        return None
    if referer_anchored_regex.search(ref):
        matches = referer_extract_regex.findall(ref)
        if len(matches):
            return matches[0]
    return None


# update page views
def channel_counts():
    while 1:
        gevent.sleep(flush_interval)
        channels = Counter()
        while 1:
            try:
                channel = channel_queue.get_nowait()
                channels[channel] += 1
            except queue.Empty:
                break
            except Exception as e:
                logger.exception(e)
                break
        if len(channels):
            gevent.spawn(update_channels, channels)


# update videos
def video_counts():
    while 1:
        gevent.sleep(flush_interval)
        videos = Counter()
        while 1:
            try:
                video = video_queue.get_nowait()
                videos[video] += 1
            except queue.Empty:
                break
            except Exception as e:
                logger.exception(e)
                break
        if len(videos):
            gevent.spawn(update_videos, videos)


# update video ads
def video_ad_counts():
    while 1:
        gevent.sleep(flush_interval)
        video_ads = Counter()
        while 1:
            try:
                ad = video_ad_queue.get_nowait()
                video_ads[ad] += 1
            except queue.Empty:
                break
            except Exception as e:
                logger.exception(e)
                break
        if len(video_ads):
            gevent.spawn(update_video_ads, video_ads)


# create the wait loops
gevent.spawn(channel_counts)
gevent.spawn(video_counts)
gevent.spawn(video_ad_counts)


# main loop
def application(env, start_response):
    # get the request path
    path = env["PATH_INFO"].lower()

    # get the query params
    try:
        params = parse_qs(env["QUERY_STRING"])
    except KeyError:
        params = None

    # get the http referer header
    referer = get_referer(env)

    # update page views
    if path == "/pageview.gif" and referer:
        start_response("200 OK", [("Content-Type", "image/gif")])
        yield gif
        channel_queue.put(referer)

    # update videos
    elif path == "/video.gif" and referer and params:
        start_response("200 OK", [("Content-Type", "image/gif")])
        yield gif
        video = params.get("video", [None])[0]
        event = params.get("event", [None])[0]
        video_queue.put((video, event))

    # update video ads
    elif path == "/video-ad.gif" and referer and params:
        start_response("200 OK", [("Content-Type", "image/gif")])
        yield gif
        video = params.get("video_ad", [None])[0]
        event = params.get("event", [None])[0]
        video_ad_queue.put((video, event))

    # read page views
    elif path == "/pageview.json" and params:
        channel = params.get("channel", [None])[0]
        res, ok = read_channels(channel)
        if ok:
            start_response("200 OK", [("Content-Type", "application/json")])
        else:
            start_response("400 Bad Request", [("Content-Type", "application/json")])
        yield json.dumps(res)

    # read videos
    elif path == "/video.json" and params:
        video = params.get("video", [None])[0]
        event = params.get("event", [None])[0]
        res, ok = read_videos(video, event)
        if ok:
            start_response("200 OK", [("Content-Type", "application/json")])
        else:
            start_response("400 Bad Request", [("Content-Type", "application/json")])
        yield json.dumps(res)

    # read video ads
    elif path == "/video-ad.json" and params:
        video = params.get("video_ad", [None])[0]
        event = params.get("event", [None])[0]
        res, ok = read_video_ads(video, event)
        if ok:
            start_response("200 OK", [("Content-Type", "application/json")])
        else:
            start_response("400 Bad Request", [("Content-Type", "application/json")])
        yield json.dumps(res)

    # bologna
    else:
        start_response("403 Forbidden", [("Content-Type", "text/plain")])
        yield "(\/) (°,,,°) (\/)"
