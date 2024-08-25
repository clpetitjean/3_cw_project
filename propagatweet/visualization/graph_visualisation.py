"""Displays the retweeting users graph legibly"""
import networkx as nx      # networkx is used in the function display_graph()
from propagatweet.twitter_collection.retweeters_collection import *
import matplotlib.pyplot as plt


def display_graph(network, mother_tweets, color):
    """Displays the retweeting users graph obtained from mother_tweets
    with color for the tweets in mother_tweets

    Parameters
    ----------
    network : dict
              networkx oriented multigraph
              The graph to display

    mother_tweets : list
                    List of statuses corresponding to the initial tweets
                    from which network was created

    color : str
            The color or color code of the initial tweets

    Returns
    ---------
    None"""

    mother_names = [mother_tweet['user']['screen_name'] for mother_tweet in mother_tweets]

    pos = nx.nx_pydot.graphviz_layout(network)
    labels = {n: n for n in network}
    nx.draw_networkx_nodes(network, pos, nodelist=mother_names, node_color=color)
    nx.draw_networkx_nodes(network, pos, nodelist=network.nodes()-mother_names, node_color='yellow')
    nx.draw_networkx_labels(network, pos, labels, font_size=7)
    nx.draw_networkx_edges(network, pos, connectionstyle='arc3,rad=0.1')


if __name__ == '__main__':
    mother_tweets = [get_tweet_from_id(1592528139862872067), get_tweet_from_id(1592559168451645440)]
    display_graph(retweeter_graph(mother_tweets, max_rt=10), mother_tweets, 'red')
    plt.show()
