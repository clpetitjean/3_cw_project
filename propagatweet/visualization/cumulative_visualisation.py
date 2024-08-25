"""Allows to plot the cumulative and instantaneous number of retweets in function
    of the time"""
import pandas as pd     # pandas is used in the function plot_cumulative_retweets()
import matplotlib.pyplot as plt
from propagatweet.utils.conversion import *
from src.env import *


def plot_cumulative_retweets(df):
    """
        plots the cumulative and instantaneous number of retweets in function of the time

        Parameters
        ----------
        df : pandas.dataframe of retweets of a same tweet

    """
    if len(df) > 0:
        tr = pd.Series(data=df['id'].values,
                         index=df['created_at'])

        grouped = tr.groupby('created_at').count()
        cumulative = tr.groupby('created_at').count().cumsum()

        cumulative.plot(label='Total Retweets', legend=True)
        grouped.plot(label='Instantaneous Retweets', legend=True, style='o')

    plt.xlabel('Date & Time')
    plt.ylabel('Number of retweets')

    plt.xticks(rotation=45)
    plt.show()


if __name__ == '__main__':
    df = json_to_dataframe(PATH_DATA_JSON)
    plot_cumulative_retweets(df)
