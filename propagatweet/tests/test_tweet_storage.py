"""test"""

from propagatweet.twitter_collection.tweet_collection import *
from propagatweet.twitter_connect.tweet_storage import *
from propagatweet.env import *


def test_store_tweets():
    """
        function that tests the store_tweets() function:
            must save the json file with the desired path

    """

    store_tweets(get_tweet_from_hashtag('#flatearth'), 'flatearth')
    # fetch tweets using #flatearth, and name file tweets_flatearth.json

    assert (Path(PATH_DATA) / 'tweets_flatearth.json').exists()
