"""Allows the creation of a graph of the network of retweeters from given initial tweets"""
from collections import deque
import networkx as nx
from propagatweet.twitter_collection.tweet_collection import *


def retweeter_graph(mother_tweets, impactful_count=0, max_rt=70):
    """
        plots a graph of retweets of one mother tweet

        Parameters
        ----------
        mother_tweets : [Status], list of tweets

        impactful_count : int, a minimum of retweets necessary in order for the function
                          to consider the tweet,
                          default = 0

        max_rt : int, the maximum number of retweets retrieved for each tweet

        Returns
        -------
        network : networkx graph, graph of the screen_names of retweeters

    """
    network = nx.MultiDiGraph()
    Q = deque()
    Q.extend(mother_tweets)

    while len(Q) > 0:
        mother_tweet = Q.popleft()
        mother_name = mother_tweet['user']['screen_name']#+mother_tweet['id_str']
        if mother_name not in network.nodes():
            network.add_node(mother_name) #on ajoute le node mother

        retweets_tweets = get_retweets_from_tweet(mother_tweet['id'], max_rt)
        #on récupère les retweets
        quoted_tweets = get_quote_from_tweet(mother_tweet['id'])
        #on récupère les quotes tweets
        if len(retweets_tweets) + len(quoted_tweets) >= impactful_count:
            #si le tweet est impactful on s'intéresse à ses retweets, sinon on arrête la branche ici
            #cela correspond à notre cas général
            for tweet in retweets_tweets:
                #pour chaque retweet/quote on crée un node et on le relie au tweet initial
                new_node_name = tweet['user']['screen_name']#+tweet['id_str']
                if new_node_name not in network.nodes():
                    #si ce n'est pas un user déjà rencontré
                    network.add_node(new_node_name)
                network.add_edge(mother_name, new_node_name)

            for tweet in quoted_tweets:
                new_node_name = tweet['user']['screen_name']#+tweet['id_str']
                if new_node_name not in network.nodes(): #si ce n'est pas un user déjà rencontré
                    network.add_node(new_node_name)
                network.add_edge(mother_name, new_node_name)

                Q.append(tweet)
    return network
