"""Tests propagatweet.twitter_collection.tweet_collection"""

from propagatweet.twitter_collection.tweet_collection import *


def test_get_tweet_from_user():
    """
        test function of get_tweet_from_user() using emmanuelmacron as user screen_name

    """
    tweets = get_tweet_from_user('emmanuelmacron')
    for tweet in tweets:
        assert 'emmanuelmacron' == tweet['user']['screen_name'].lower()


def test_get_tweet_from_keyword():    #sometimes this test does not work, because the twitter API collects tweets without the keyword
    """
        test function of get_tweet_from_keyword() using fake as common keyword of tweets

    """
    tweets = get_tweet_from_keyword('fake')
    for tweet in tweets:
        assert 'fake' in tweet['full_text'].lower()

def test_get_tweet_from_hashtag():
    """
        test function of get_tweet_from_hashtag() using #wrong as common hashtag of tweets

    """
    tweets = get_tweet_from_hashtag('#wrong')
    L=[]
    for i in range(len(tweets[0]['entities']['hashtags'])):
        L.append(tweets[0]['entities']['hashtags'][i]['text'].lower())
    assert 'wrong' in L


def test_get_tweet_from_id():
    """
        test function of get_tweet_from_id() using 1589987021439008770 as id

    """
    tweet = get_tweet_from_id(1589987021439008770)
    assert '1589987021439008770' == tweet['id_str']


def test_get_retweets_from_user():
    """
        test function of get_retweets_from_user()
        fetching the retweets of 'emmanuelmacron' 's last tweets

    """
    tweets = get_retweets_from_user('emmanuelmacron')
    for tweet in tweets:
        assert 'emmanuelmacron' == tweet['retweeted_status']['user']['screen_name'].lower()


def test_get_retweets_from_tweet():
    """
        test function of get_retweets_from_tweet()
        fetching the retweets of the 1589987021439008770(tweet_id) tweet

    """
    tweets = get_retweets_from_tweet(1589987021439008770)
    for tweet in tweets:
        assert '1589987021439008770' == tweet['retweeted_status']['id_str']
