"""Tests propagatweet.twitter_connect.twitter_connection_setup"""
from propagatweet.twitter_connect.twitter_connection_setup import *


def test_twitter_setup():
    """
        function that tests the twitter_setup() function:
            must not return None
            must return a tweepy.API type

    """
    assert twitter_setup() is not None
    assert isinstance(twitter_setup(), tweepy.API)
