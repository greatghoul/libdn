#-*- coding: utf-8 -*-

""" Parsers for feeds and webpages """

import feedparser

class Feed(object):
    def __init__(self, feedurl, title, link):
        self.feedurl = feedurl
        self.title = title
        self.link = link
        self.wallpapers = []

class Wallpaper(object):
    def __init__(self, title, pub_date, link):
        self.title = title
        self.pub_date = pub_date
        self.link = link

class FeedParser(object):
    def __init__(self, feedurl):
        self.feedurl = feedurl
        
    def load(self):
        doc = feedparser.parse(self.feedurl)
        feed = Feed(self.feedurl, doc.feed.title, doc.feed.link)
        for entry in doc.entries:
            wallpaper = Wallpaper(entry.title, entry.published, entry.link)
            feed.wallpapers.append(wallpaper)
        return feed
