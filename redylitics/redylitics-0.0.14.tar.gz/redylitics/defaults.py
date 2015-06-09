#!/usr/bin/env python
# -*- coding: utf-8 -*-


# sentinels stuff

DEF_SENTINEL_HOSTS = "localhost"
DEF_SENTINEL_PORT = 26379
DEF_SENTINEL_MASTER_NAME = "mymaster"


# strict clients stuff

DEF_REDIS_HOST = "localhost"
DEF_REDIS_PORT = 6379
DEF_REDIS_DB = 0


# pageview stuff

DEF_WRITE_CHANNEL_REGEX_PATTERN = "^(theonion|avclub|clickhole|onionstudios)\\d{8}$"
DEF_WRITE_DATE_REGEX_PATTERN = "\\d{8}"
DEF_READ_CHANNEL_REGEX_PATTERN = "^(theonion|avclub|clickhole|onionstudios)\\d{6,}\\*?"
DEF_READ_DATE_REGEX_PATTERN = "(\\d{6}\\*|\\d{8})"
DEF_DATE_EXTRACTION_REGEX_PATTERN = "\\d{8}"


# video stuff

DEF_VIDEO_PREFIX = "video"
DEF_VIDEO_ID_REGEX_PATTERN = "\\d+"
DEF_VIDEO_EVENT_REGEX_PATTERN = "^(start|complete|firstQuartile|midpoint|thirdQuartile)$"


# video ad stuff

DEF_VIDEO_AD_PREFIX = "video_ad"
DEF_VIDEO_AD_ID_REGEX_PATTERN = "\\d+"
DEF_VIDEO_AD_EVENT_REGEX_PATTERN = "^(start|complete|firstQuartile|midpoint|thirdQuartile)$"


# wsgi stuff

DEF_REFERER_ANCHORED_REGEX_PATTERN = "(staff|www)\\.(theonion|avclub|clickhole|onionstudios)\\.com"
DEF_REFERER_EXTRACT_REGEX_PATTERN = "(theonion|avclub|clickhole|onionstudios)"
DEF_FLUSH_INTERVAL = 10
