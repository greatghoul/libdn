#-*- coding: utf-8 -*-
import sys, os
path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(path))

import unittest
from libdn.parser import FeedParser

class FeedParserTestCase(unittest.TestCase):
    def setUp(self):
        feedurl = 'http://www.desktopnexus.com/feed/'
        self.parser = FeedParser(feedurl)

    def test_load(self):
        feed = self.parser.load()
        self.assertIsNotNone(feed)
        self.assertEquals('http://www.desktopnexus.com/feed/', feed.feedurl)
        self.assertEquals('Desktop Nexus - Global Wallpaper RSS Feed', feed.title)
        self.assertEquals('http://www.desktopnexus.com', feed.link)
        self.assertEquals(20, len(feed.wallpapers))

if __name__ == '__main__':
    unittest.main()
