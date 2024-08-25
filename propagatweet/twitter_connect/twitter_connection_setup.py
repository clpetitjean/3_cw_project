"""Allows the connection to Twitter API"""
import tweepy
# We import our access keys:
from src.credentials import *

def twitter_setup():
    """
        Utility function to setup the Twitter's API
        with an access keys provided in a file credentials.py

        Returns
        -------
        api : tweepy.API, the authentified API

    """
    # Authentication and access using keys:
    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    return api


def twitter_setup_2():
    auth2 = tweepy.OAuth2BearerHandler(BEARER_TOKEN)
    auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    client = tweepy.Client(auth2)
    return client
