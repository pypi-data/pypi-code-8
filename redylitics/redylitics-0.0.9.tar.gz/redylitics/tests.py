#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from datetime import date, datetime
from unittest import TestCase

from .clients import PageviewClient, VideoClient, VideoAdClient
from .endpoints import update_channels, update_videos, update_video_ads, read_channels, read_videos, read_video_ads


class PageviewClientTests(TestCase):
    def setUp(self):
        self.client = PageviewClient()
        print(self.client.WRITE_CHANNEL_REGEX.pattern)
        print(self.client.WRITE_DATE_REGEX.pattern)
        print(self.client.READ_CHANNEL_REGEX.pattern)
        print(self.client.READ_DATE_REGEX.pattern)
        print(self.client.DATE_EXTRACTION_REGEX.pattern)

    def tearDown(self):
        self.client.connection.flushdb()
    
    def test_update_channel(self):
        # good data
        self.assertTrue(self.client.update_channel("theonion20150101", 100))
        self.assertTrue(self.client.update_channel("clickhole20150101", 100))
        self.assertTrue(self.client.update_channel("avclub20150101", 100))
        self.assertTrue(self.client.update_channel("onionstudios20150101", 100))

        with self.assertRaises(Exception):
            # bad dates - jan 99th
            self.client.update_channel("theonion20150199", 100)
            self.client.update_channel("clickhole20150199", 100)
            self.client.update_channel("avclub20150199", 100)
            self.client.update_channel("onionstudios20150199", 100)

            # incomplete dates
            self.client.update_channel("theonion201501", 100)
            self.client.update_channel("clickhole201501", 100)
            self.client.update_channel("avclub201501", 100)
            self.client.update_channel("onionstudios201501", 100)

            # bad values - strings
            self.client.update_channel("theonion20150101", "100")
            self.client.update_channel("clickhole20150101", "100")
            self.client.update_channel("avclub20150101", "100")
            self.client.update_channel("onionstudios20150101", "100")

            # bad channel name
            self.client.update_channel("barforama20150101", 100)

    def test_read_channel(self):
        _ = self.client.update_channel("theonion20170101", 100)
        _ = self.client.update_channel("theonion20170102", 100)

        # good channel keys
        data = self.client.read_channel("theonion20170101")
        self.assertEqual(data, dict([("2017-01-01", 100)]))
        data = self.client.read_channel("theonion20170102")
        self.assertEqual(data, dict([("2017-01-02", 100)]))
        data = self.client.read_channel("theonion201701*")
        self.assertAlmostEqual(data, dict([("2017-01-02", 100), ("2017-01-01", 100)]))

        with self.assertRaises(Exception):
            # bad date
            _ = self.client.read_channel("theonion20170199")

            # incomplete date
            _ = self.client.read_channel("theonion2017*")

            # bad channel name
            _ = self.client.read_channel("barforama20170101")


class VideoClientTests(TestCase):
    def setUp(self):
        self.client = VideoClient()

    def tearDown(self):
        self.client.connection.flushdb()

    def test_update_video(self):
        # good data
        self.assertTrue(self.client.update_video(123, "start", 10))
        self.assertTrue(self.client.update_video(123, "complete", 10))
        self.assertTrue(self.client.update_video(123, "firstQuartile", 10))
        self.assertTrue(self.client.update_video(123, "midpoint", 10))
        self.assertTrue(self.client.update_video(123, "thirdQuartile", 10))

        with self.assertRaises(Exception):
            # bad video id
            self.client.update_video("123", "start", 10)
            self.client.update_video("this-is-a-video", "start", 10)

            # bad event
            self.client.update_video(123, "hooray!", 1)

            # bad value
            self.client.update_video(123, "start", 1.3)

    def test_read_video(self):
        _ = self.client.update_video(312, "start", 10)
        _ = self.client.update_video(312, "complete", 10)
        _ = self.client.update_video(312, "firstQuartile", 10)
        _ = self.client.update_video(312, "midpoint", 10)
        _ = self.client.update_video(312, "thirdQuartile", 10)

        # good keys
        data = self.client.read_video(312)
        self.assertEqual(data, {"firstQuartile": 10, "start": 10, "midpoint": 10, "complete": 10, "thirdQuartile": 10})
        data = self.client.read_video(312, "start")
        self.assertEqual(data, {"start": 10})

        with self.assertRaises(Exception):
            _ = self.client.read_video("123", "start")
            _ = self.client.read_video("this-is-a-video")
            _ = self.client.read_video(312, "barf")


class VideoAdClientTests(VideoClientTests):
    def setUp(self):
        self.client = VideoAdClient()


class ReadChannelsEndpointTests(TestCase):
    def setUp(self):
        self.client = PageviewClient()

    def tearDown(self):
        self.client.connection.flushdb()

    def test_read_channels(self):
        key = "theonion20170101"
        _ = self.client.update_channel(key, 100)

        data = self.client.read_channel(key)
        self.assertEqual(data, {"2017-01-01": 100})

        res, ok = read_channels(key)
        self.assertTrue(ok)
        self.assertEqual(res, {"2017-01-01": 100})


class ReadVideoEndpointTests(TestCase):
    def setUp(self):
        self.client = VideoClient()

    def tearDown(self):
        self.client.connection.flushdb()

    def test_read_videos(self):
        _ = self.client.update_video(312, "start", 10)
        _ = self.client.update_video(312, "complete", 10)
        _ = self.client.update_video(312, "firstQuartile", 10)
        _ = self.client.update_video(312, "midpoint", 10)
        _ = self.client.update_video(312, "thirdQuartile", 10)

        data = self.client.read_video(312)
        self.assertEqual(data, {"firstQuartile": 10, "start": 10, "midpoint": 10, "complete": 10, "thirdQuartile": 10})

        res, ok = read_videos(312)
        self.assertTrue(ok)
        self.assertEqual(res, {"firstQuartile": 10, "start": 10, "midpoint": 10, "complete": 10, "thirdQuartile": 10})


class ReadVideoAdEndpointTests(TestCase):
    def setUp(self):
        self.client = VideoAdClient()

    def tearDown(self):
        self.client.connection.flushdb()

    def test_read_video_ads(self):
        _ = self.client.update_video(312, "start", 10)
        _ = self.client.update_video(312, "complete", 10)
        _ = self.client.update_video(312, "firstQuartile", 10)
        _ = self.client.update_video(312, "midpoint", 10)
        _ = self.client.update_video(312, "thirdQuartile", 10)

        data = self.client.read_video(312)
        self.assertEqual(data, {"firstQuartile": 10, "start": 10, "midpoint": 10, "complete": 10, "thirdQuartile": 10})

        res, ok = read_video_ads(312)
        self.assertTrue(ok)
        self.assertEqual(res, {"firstQuartile": 10, "start": 10, "midpoint": 10, "complete": 10, "thirdQuartile": 10})


class UpdateChannelsTests(TestCase):
    def setUp(self):
        self.client = PageviewClient()

    def tearDown(self):
        self.client.connection.flushdb()

    def test_update_channels(self):
        page_views = Counter({"theonion": 100})
        results = update_channels(page_views)
        for res in results:
            self.assertTrue(res)

        t = date.today()
        today = datetime(t.year, t.month, t.day).strftime("%Y%m%d")
        key = "theonion{}".format(today)
        data = self.client.read_channel(key)

        key = datetime(t.year, t.month, t.day).strftime("%Y-%m-%d")
        self.assertEqual(data, {key: 100})


class UpdateVideosTests(TestCase):
    def setUp(self):
        self.client = VideoClient()

    def tearDown(self):
        self.client.connection.flushdb()

    def test_update_videos(self):
        videos = Counter({
            (312, "start"): 10,
            (312, "complete"): 10,
            (312, "firstQuartile"): 10,
            (312, "midpoint"): 10,
            (312, "thirdQuartile"): 10,
        })
        results = update_videos(videos)
        for res in results:
            self.assertTrue(res)

        data = self.client.read_video(312)
        self.assertEqual(data, {"firstQuartile": 10, "start": 10, "midpoint": 10, "complete": 10, "thirdQuartile": 10})


class UpdateVideoAdsTests(TestCase):
    def setUp(self):
        self.client = VideoAdClient()

    def tearDown(self):
        self.client.connection.flushdb()

    def test_update_videos(self):
        ads = Counter({
            (312, "start"): 10,
            (312, "complete"): 10,
            (312, "firstQuartile"): 10,
            (312, "midpoint"): 10,
            (312, "thirdQuartile"): 10,
        })
        results = update_video_ads(ads)
        for res in results:
            self.assertTrue(res)

        data = self.client.read_video(312)
        self.assertEqual(data, {"firstQuartile": 10, "start": 10, "midpoint": 10, "complete": 10, "thirdQuartile": 10})
