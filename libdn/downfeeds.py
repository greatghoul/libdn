#-*- coding: utf-8 -*-
import logging.config
logging.config.fileConfig('logging.cfg')

from optparse import OptionParser

import os, codecs, re, logging
import urllib, urllib2, cookielib, urlparse, feedparser

DEFAULT_RESOLUTION = '1024x768'
DOWNLOAD_DIR = 'wallpapers'

def initial():
    # make wallpaper download dir
    if not os.path.exists(DOWNLOAD_DIR):
        os.mkdir(DOWNLOAD_DIR)

    # Config cookie
    cookie = cookielib.CookieJar()
    processer = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(processer)
    urllib2.install_opener(opener)

def get_pic_info(url):
    pic_id = url.split('/')[-2]
    html = urllib2.urlopen(url).read()
    pattern = r'<a href=\"\/get\/%s\/\?t=(?P<token>.*?)\"' % pic_id
    match = re.search(pattern, html, flags=re.I|re.M|re.S)
    if match:
        return { 'id': pic_id, 'token': match.group('token'), 'size': options.size }

def get_pic_file(pic_info):
    redirect_url = 'http://www.desktopnexus.com/dl/inline/%(id)s/%(size)s/%(token)s' % pic_info
    request = urllib2.urlopen(redirect_url)
    return request.geturl()

def download_pic(url):
    pic_info = get_pic_info(url)
    pic_file = get_pic_file(pic_info)
    filename = os.path.split(urlparse.urlparse(pic_file).path)[-1]
    logging.info('  Saving file: %s' % filename)
    open(os.path.join(os.path.abspath(DOWNLOAD_DIR),filename), 'wb').write(urllib2.urlopen(pic_file).read())

def readfeeds(feedurl):
    try:
        doc = feedparser.parse(feedurl)
        entrie_count = len(doc.entries)

        # Output feed infomation
        logging.info('  Feed Name: %s' % doc.feed.title)
        logging.info('  Feed Description: %s' % doc.feed.description)
        logging.info('  Feed Entries Count: %d' % entrie_count)

        # Loop download all wallpapers
        logging.info('Start Fetching wallpapers')
        for i, item in enumerate(doc.entries):
            logging.info('  Fetching Wallpaper[%2d/%d]: %s' % (i + 1, entrie_count, item.title))
            try:
                download_pic(item.link)
            except Exception as e:
                logging.error('  Error: %s' % e)
    except Exception as e:
        logging.error(e)

if __name__ == '__main__':
    # Setup optparser
    parser = OptionParser()
    parser.add_option('-f', '--feed', dest='feed', help='specific a feed url')
    parser.add_option('-p', '--page', dest='page', help='specific a page that includes wallpaper list')
    parser.add_option('-s', '--size', dest='size', help='specific the wallpaper size, default 1440x900', default='1440x900')
    (options, args) = parser.parse_args()

    logging.info('Initial enviroment..')
    initial()

    if options.feed:
        logging.info('Reading feed: ' + options.feed)
        readfeeds(options.feed)
