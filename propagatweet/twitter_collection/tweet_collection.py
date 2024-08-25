"""Allows the collection of tweets having some given parameters"""
import requests
import tweepy
import time
from propagatweet.twitter_connect.twitter_connection_setup import *
from src.credentials import *


def get_tweet_from_user(screen_name, count_tweets=20):
    """
        function that gives the most recent tweets from a user

        Parameters
        ----------
        screen_name : str, screen name of the user from which we want to collect tweets

        count_tweets : int, number of tweets from that user we want to collect, default = 20

        Returns
        -------
        tweets : [Status], fetched tweets from user as status

    """
    api = twitter_setup()
    try:
        tweets = api.user_timeline(screen_name=screen_name, count=count_tweets,
                                   tweet_mode='extended')

    except tweepy.errors.TooManyRequests:
        print('Too many requests, try again later')
        return []

    return tweets


def get_tweet_from_keyword(keyword, count_tweets=5000):
    """
        function that gives the most recent tweets from a keyword, without metadata

        Parameters
        ----------
        keyword : str, keyword around which we want to search tweets

        count_tweets : int, number of tweets with that keyword we want to collect, default = 20

        Returns
        -------
        tweets : [Status], Fetched tweets containing the keyword

    """
    api = twitter_setup()
    try:
        search_results = api.search_tweets(q=keyword + ' -filter:retweets',
                                           count=count_tweets, lang='en', tweet_mode='extended')
        tweets = search_results['statuses']

    except tweepy.errors.TooManyRequests:
        print('Too many requests, try again later')
        return []

    return tweets


def get_tweet_from_hashtag(hashtag, count_tweets=5000):
    """
        function that gives the most recent tweets from a hashtag, without metadata

        Parameters
        ----------
        hashtag : str, hashtag from which we want to collect tweets, ex = '#flatearth'

        count_tweets : int, number of tweets with that hashtag we want to collect, default = 20

        Returns
        -------
        tweets : [Status], Fetched tweets containing the hashtag

    """
    api = twitter_setup()
    try:
        hashtag = hashtag.replace('#', '%23')
        tweets = api.search_tweets(q=hashtag + ' -filter:retweets', count=count_tweets,
                                   lang='fr', until=2023 - 2 - 8, tweet_mode='extended')['statuses']
    except tweepy.errors.TooManyRequests:
        print('Too many requests, try again later')
        return []
    return tweets


def get_tweet_from_id(tweet_id):
    """
        function that gives the tweet corresponding to the given tweet_id

        Parameters
        ----------
        tweet_id : int, id of the tweet we want to collect

        Returns
        -------
        tweets : Status, tweet with id=tweet_id

    """
    api = twitter_setup()
    try:
        tweet = api.get_status(tweet_id, tweet_mode='extended')
    except tweepy.errors.TooManyRequests:
        print('Too many requests, try again later')
        return None
    else:
        return tweet


def get_retweets_from_user(screen_name, count_tweets=10, count_retweets=10):
    """
        function that gives the most recent retweets from a user, without metadata

        Parameters
        ----------
        screen_name : str, screen_name of the user we are interested in

        count_tweets : int, number of tweets from that user we want to collect, default = 10

        count_retweets : int, number of retweets from each tweet we want to collect, default = 10

        Returns
        -------
        all_retweets : [Status], tweets starting with "RT @" : list of retweets to the user last tweets

    """
    api = twitter_setup()
    all_retweets = []
    try:
        tweets = api.user_timeline(screen_name=screen_name, count=count_tweets,
                                   include_rts=False, tweet_mode='extended')
        for tweet in tweets:
            tweet_id = tweet['id']
            try:
                retweets = api.get_retweets(id=tweet_id, count=count_retweets, tweet_mode='extended')
            except tweepy.errors.TweepyException as e:
                print(e)
            else:
                all_retweets.extend(retweets)
    except tweepy.errors.TooManyRequests:
        print('Too many requests, try again later')
    return all_retweets


def get_retweets_from_tweet(tweet_id, count_retweets=20):
    """
        function that gives the most recent retweets to a tweet, without metadata

        Parameters
        ----------
        tweet_id : int, id of a tweet

        count_retweets : int, number of retweets we want to collect, default = 20

        Returns
        -------
        retweets : [Status], tweets starting with "RT @" :
                 list of retweets to tweet with the given tweet_id

    """
    api = twitter_setup()
    try:
        retweets = api.get_retweets(id=tweet_id, count=count_retweets, tweet_mode='extended')
    except tweepy.errors.TooManyRequests:
        print('Too many requests, try again later')
        return []
    return retweets


def get_quote_from_tweet(tweet_id, count_tweets=100):
    """
        function that gives the quoted tweets from a single tweet

        Parameters
        ----------
        tweet_id : int, id of a tweet

        count_tweets : int
                        Number of tweets to get, max 100

        Returns
        -------
        tweets : [Status], tweets that quote the tweet_id

    """
    url = "https://api.twitter.com/2/tweets/{}/quote_tweets".format(tweet_id)
    param = {"tweet.fields": 'author_id,id', 'max_results': count_tweets}
    headers = {"Authorization": "Bearer {}".format(BEARER_TOKEN)}
    tweets = []
    try:
        quote = requests.request("GET", url, headers=headers, params=param)
        api = twitter_setup()
        result = quote.json()
        if 'meta' in result.keys() and result['meta']['result_count'] > 0:
            for tweet in quote.json()['data']:
                try:
                    status = api.get_status(tweet['id'], tweet_mode='extended')
                except tweepy.errors.TweepyException as e:
                    print(e)
                else:
                    tweets.append(status)
    except tweepy.errors.TooManyRequests:
        print('Too many requests, try again later')
        return tweets
    except tweepy.errors.TweepyException as e:
        print(e)
    return tweets


def get_many_tweets_from_keyword(keyword):
    client = tweepy.Client(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token = ACCESS_TOKEN, access_token_secret = ACCESS_SECRET, bearer_token=BEARER_TOKEN)
    tweets = []
    try:
        search_results = tweepy.Paginator(client.search_recent_tweets, query=keyword + ' -is:retweet', max_results=100)

        for tweet in search_results.flatten(5000):
            tweets.append(tweet.text)

    except tweepy.errors.TooManyRequests:
        print('Too many requests, try again later')
        return []

    return tweets


def get_many_tweets_from_hashtag(hashtag):
    client = tweepy.Client(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token = ACCESS_TOKEN, access_token_secret = ACCESS_SECRET, bearer_token=BEARER_TOKEN)
    tweets=[]
    try:
        hashtag = hashtag.replace('#', '%23')
        search_results = tweepy.Paginator(client.search_recent_tweets, query=hashtag + ' -is:retweet', max_results=100)

        for tweet in search_results.flatten(5000):
            tweets.append(tweet.text)

    except tweepy.errors.TooManyRequests:
        print('Too many requests, try again later')
        return []

    return tweets


if __name__ == '__main__':
    print(get_many_tweets_from_hashtag('Little Mermaid'))
