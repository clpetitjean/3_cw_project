"""Plots the amount of a given characteristic of tweets in function of the time"""
import pandas as pd            # pandas is used in the function plot_time_series()
import matplotlib.pyplot as plt
from propagatweet.utils.conversion import *
from src.env import *


def plot_time_series(df, column, label):
    """
        plots the amount of a given characteristic of tweets in function of the time

        Parameters
        ----------
        df : pandas.dataframe of tweets

        column : str, the characteristic that is plotted

        label : str, the label of the characteristic

    """
    tfav = pd.Series(data=df[column].values,
                     index=df['created_at'])
    tfav.plot(figsize=(12, 6), label=label, legend=True)
    plt.xticks(rotation=45)
    plt.show()


if __name__ == '__main__':
    df = json_to_dataframe(PATH_DATA_JSON)
    print(df)
    plot_time_series(df, 'favorite_count', 'Likes')
