""" stores anagrams into memcache """

import random
import re

import worldnews
#import pyanagrams
from google.appengine.api import memcache

def preparefood():
    words, feed = worldnews.getwords()
    randkey = str(random.randrange(111111,999999))
    seedfood = " ".join(words)
    # food = pyanagrams.getanagrams(seedfood)
    memcache.set(randkey, None, 18000)
    return randkey, seedfood, words, feed

def customfood(word):
    randkey = str(random.randrange(111111,999999))
    strlist = re.split(r"[^a-z^A-Z]",word)
    seedfood = "".join(word)
    # food = pyanagrams.getanagrams(seedfood)
    memcache.set(randkey, None, 18000)
    return randkey, seedfood
    
