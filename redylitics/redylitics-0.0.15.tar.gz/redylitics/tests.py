#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from datetime import date, datetime
from unittest import TestCase

from .clients import SentinelClient
from .config import *
from .endpoints import update_channels, update_videos, update_video_ads, read_channels, read_videos, read_video_ads
from .wsgi import get_referer


class SentinelClientTests(TestCase):
    def setUp(self):
        self.client = SentinelClient(SENTINEL_HOSTS, SENTINEL_PORT, SENTINEL_MASTER_NAME)

    def tearDown(self):
        self.client.sentinel.get_master().flushdb()

    def test_set(self):
        result = self.client.set_one("test", 1)
        self.assertEqual(result, 1)

    def test_set_hash(self):
        result = self.client.set_one_hash("test-hash", "test", 1)
        self.assertEqual(result, 1)

    def test_get_one(self):
        _ = self.client.set_one("test", 1)
        result = self.client.get_one("test")
        self.assertEqual(result, 1)

    def test_get_many(self):
        _ = self.client.set_one("multi1", 1)
        _ = self.client.set_one("multi2", 1)
        _ = self.client.set_one("multi3", 1)
        result = self.client.get_many("multi*")
        self.assertEqual(result, [("multi1", 1), ("multi2", 1), ("multi3", 1)])

    def test_get_one_hash(self):
        _ = self.client.set_one_hash("test-hash", "test", 1)
        result = self.client.get_one_hash("test-hash")
        self.assertEqual(result, {"test": 1})
        result = self.client.get_one_hash("test-hash", ["test", ])
        self.assertEqual(result, {"test": 1})


class RefererTests(TestCase):
    def test_get_referer(self):
        good_referers = (
            "http://www.theonion.com/articles/blah-123",
            "http://www.avclub.com/videos/blah-123",
            "http://www.clickhole.com/quizzes/blah-123",
            "http://www.onionstudios.com/channels/the-onion",
        )
        bad_referers = (
            "http://barf.theonion.com/articles/blah-123",
            "http://puke.avclub.com/videos/blah-123",
            "http://hurl.clickhole.com/quizzes/blah-123",
            "http://yuck.onionstudios.com/channels/the-onion",
            "http://www.barftheonion.com/articles/blah-123",
            "http://www.pukeavclub.com/videos/blah-123",
            "http://www.hurlclickhole.com/quizzes/blah-123",
            "http://www.yuckonionstudios.com/channels/the-onion",
            "http://theonion.local/articles/blah-123",
            "http://avclub.local/videos/blah-123",
            "http://clickhole.local/quizzes/blah-123",
            "http://onionstudios.local/channels/the-onion",
        )
        for ref in good_referers:
            self.assertIsNotNone(get_referer({"HTTP_REFERER": ref}))
        for ref in bad_referers:
            self.assertIsNone(get_referer({"HTTP_REFERER": ref}))


class ReadChannelsEndpointTests(TestCase):
    def setUp(self):
        self.client = SentinelClient(SENTINEL_HOSTS, SENTINEL_PORT, SENTINEL_MASTER_NAME)

    def tearDown(self):
        self.client.sentinel.get_master().flushdb()

    def test_read_channels(self):
        key = "theonion20170101"
        _ = self.client.set_one(key, 100)

        data = self.client.get_one(key)
        self.assertEqual(data, 100)

        res, ok = read_channels(key)
        print(res)
        self.assertTrue(ok)
        self.assertEqual(res, {"2017-01-01": 100})


class ReadVideoEndpointTests(TestCase):
    def setUp(self):
        self.client = SentinelClient(SENTINEL_HOSTS, SENTINEL_PORT, SENTINEL_MASTER_NAME)

    def tearDown(self):
        self.client.sentinel.get_master().flushdb()

    def test_read_videos(self):
        _ = self.client.set_one_hash("video.312", "start", 10)
        _ = self.client.set_one_hash("video.312", "complete", 10)
        _ = self.client.set_one_hash("video.312", "firstQuartile", 10)
        _ = self.client.set_one_hash("video.312", "midpoint", 10)
        _ = self.client.set_one_hash("video.312", "thirdQuartile", 10)

        data = self.client.get_one_hash("video.312")
        self.assertEqual(data, {"firstQuartile": 10, "start": 10, "midpoint": 10, "complete": 10, "thirdQuartile": 10})

        res, ok = read_videos("312")
        self.assertTrue(ok)
        self.assertEqual(res, {"firstQuartile": 10, "start": 10, "midpoint": 10, "complete": 10, "thirdQuartile": 10})


class ReadVideoAdEndpointTests(TestCase):
    def setUp(self):
        self.client = SentinelClient(SENTINEL_HOSTS, SENTINEL_PORT, SENTINEL_MASTER_NAME)

    def tearDown(self):
        self.client.sentinel.get_master().flushdb()

    def test_read_video_ads(self):
        _ = self.client.set_one_hash("video_ad.312", "start", 10)
        _ = self.client.set_one_hash("video_ad.312", "complete", 10)
        _ = self.client.set_one_hash("video_ad.312", "firstQuartile", 10)
        _ = self.client.set_one_hash("video_ad.312", "midpoint", 10)
        _ = self.client.set_one_hash("video_ad.312", "thirdQuartile", 10)

        data = self.client.get_one_hash("video_ad.312")
        self.assertEqual(data, {"firstQuartile": 10, "start": 10, "midpoint": 10, "complete": 10, "thirdQuartile": 10})

        res, ok = read_video_ads("312")
        self.assertTrue(ok)
        self.assertEqual(res, {"firstQuartile": 10, "start": 10, "midpoint": 10, "complete": 10, "thirdQuartile": 10})


class UpdateChannelsTests(TestCase):
    def setUp(self):
        self.client = SentinelClient(SENTINEL_HOSTS, SENTINEL_PORT, SENTINEL_MASTER_NAME)

    def tearDown(self):
        self.client.sentinel.get_master().flushdb()

    def test_update_channels(self):
        page_views = Counter({"theonion": 100})
        _ = update_channels(page_views)

        t = date.today()
        today = datetime(t.year, t.month, t.day).strftime("%Y%m%d")
        key = "theonion{}".format(today)
        data = self.client.get_one(key)
        self.assertEqual(data, 100)


class UpdateVideosTests(TestCase):
    def setUp(self):
        self.client = SentinelClient(SENTINEL_HOSTS, SENTINEL_PORT, SENTINEL_MASTER_NAME)

    def tearDown(self):
        self.client.sentinel.get_master().flushdb()

    def test_update_videos(self):
        videos = Counter({
            ("312", "start"): 10,
            ("312", "complete"): 10,
            ("312", "firstQuartile"): 10,
            ("312", "midpoint"): 10,
            ("312", "thirdQuartile"): 10,
        })
        _ = update_videos(videos)

        data = self.client.get_one_hash("video.312")
        self.assertEqual(data, {"firstQuartile": 10, "start": 10, "midpoint": 10, "complete": 10, "thirdQuartile": 10})


class UpdateVideoAdsTests(TestCase):
    def setUp(self):
        self.client = SentinelClient(SENTINEL_HOSTS, SENTINEL_PORT, SENTINEL_MASTER_NAME)

    def tearDown(self):
        self.client.sentinel.get_master().flushdb()

    def test_update_videos(self):
        ads = Counter({
            ("312", "start"): 10,
            ("312", "complete"): 10,
            ("312", "firstQuartile"): 10,
            ("312", "midpoint"): 10,
            ("312", "thirdQuartile"): 10,
        })
        _ = update_video_ads(ads)

        data = self.client.get_one_hash("video_ad.312")
        self.assertEqual(data, {"firstQuartile": 10, "start": 10, "midpoint": 10, "complete": 10, "thirdQuartile": 10})
