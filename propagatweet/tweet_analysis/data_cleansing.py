import re
import emoji
import nltk
from propagatweet.utils.conversion import *
from src.env import *


def cleaner_tweets(tweet):
    words = set(nltk.corpus.words.words())
    tweet = re.sub("@[A-Za-z0-9]+","",tweet)
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet)
    tweet = " ".join(tweet.split())
    tweet = ''.join(c for c in tweet if c not in emoji.EMOJI_DATA)
    tweet = tweet.replace("#", "").replace("_", " ")
    tweet = " ".join(w for w in nltk.wordpunct_tokenize(tweet) if w.lower() in words or not w.isalpha())
    return tweet


def cleaner_df(df):
    df['full_text'] = df['full_text'].map(lambda x: cleaner_tweets(x))
    return df


if __name__ == '__main__':
    df = json_to_dataframe(PATH_DATA_JSON)
    df = cleaner_df(df)
    print(df['full_text'])

