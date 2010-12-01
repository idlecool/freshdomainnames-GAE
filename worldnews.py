#!/usr/bin/env python
""" retrieve random words from news feeds """

import urllib
import random
import re

from BeautifulSoup import BeautifulStoneSoup

stream = ""


def _worldnews():
    # webservice = 'http://www.thehindu.com/sci-tech/technology/?service=rss'
    webservice = 'http://www.thehindu.com/news/international/?service=rss'
    global stream
    if stream == "":
        stream = urllib.urlopen(webservice).read()
    soup = BeautifulStoneSoup(stream)
    feedtitles = soup.findAll('title')
    feedlinks = soup.findAll('link')
    feeddescriptions = soup.findAll('description')
    feeds = [feedtitles, feedlinks, feeddescriptions]
    return feeds


def _randomfeed():
    feeds = _worldnews()
    [feedtitles, feedlinks, feeddescriptions] = feeds
    numfeed = len(feedtitles)
    anyfeed = random.randrange(1,numfeed)
    feedtitle = feedtitles[anyfeed]
    feedlink = feedlinks[anyfeed]
    feeddescription = feeddescriptions[anyfeed]
    feedtitlestr = feedtitle.string.encode('utf-8')
    feedlinkstr = feedlink.string.encode('utf-8')
    feeddescriptionstr = feeddescription.prettify().split("\n")[2]
    feed = [feedtitlestr, feedlinkstr, feeddescriptionstr ]
    return feed


def _getproperwords():
    feed = _randomfeed()
    [feedstring, feedlink, feeddescription ] = feed
    stringaslist = re.split(r"[^a-z^A-Z]",feedstring)
    for num in xrange(stringaslist.count("")):
        stringaslist.remove("")
    properwords = []
    for word in stringaslist:
        if len(word) > 4 and len(word) < 10:
            properwords.append(word)
    return properwords, feed


def getwords():
    properwords, feed = _getproperwords()
    while(len(properwords) < 2):
        properwords, feedstring = _getproperwords()
    feedlen = len(properwords)
    words = []
    word1 = properwords[random.randrange(0,feedlen)]
    #properwords.remove(word1)
    #word2 = properwords[random.randrange(0,feedlen-1)]
    words.extend([word1,])
    return words, feed


if __name__ == "__main__":
    words, feed = getwords()
    print  words[0], ",", words[1]
    print "have been selected from:", feed[0]
    print feed[1]
    print feed[2]
