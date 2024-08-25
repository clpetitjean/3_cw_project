"""Allows to retrieve tweets and save them in a json file"""
import json
from propagatweet.utils.path_management import *
from propagatweet.twitter_collection import tweet_collection


def tweet_file_name(filename, extension):
    """
        gives the full saving name for a file of tweets

        Parameters
        ----------
        filename : str
                   name of the file
        extension: str
                   extension of the file

        Returns
        -------
        a str full name of the saved file
    """
    return "tweets_" + "_".join(filename.split(" ")) + extension


def store_tweets(tweets, filename):
    """
        saves the tweets in a json file 'tweets_filename.json'

        Parameters
        ----------
        tweets : [Status], given by a function in twitter_collection.tweet_collection

        filename : str, subject of the tweets

    """
    name = tweet_file_name(filename, ".json")
    file = get_file_path_data(name)
    file_open = open(file, "w")
    json.dump(tweets, file_open, indent=4)


if __name__ == "__main__":
    HASHTAG = 'AsterixetObelixlempireDuMilieu'
    tweets = tweet_collection.get_many_tweets_from_hashtag(HASHTAG)
    store_tweets(tweets, HASHTAG)
