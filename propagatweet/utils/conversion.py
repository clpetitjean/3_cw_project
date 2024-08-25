"""Allows to convert different files in pandas dataframes"""
import pandas as pd


def json_to_dataframe(filename, useful_datas=None):
    """
        converts a json file into a pandas.dataframe

        Parameters
        ----------
        filename : str, path to json file

        useful_datas : [str] of the columns we want to keep in the pandas.dataframe,
                       default = None (all are kept)

        Returns
        -------
        df : pandas.dataframe of given data

    """
    df = pd.read_json(filename)
    if useful_datas is not None:
        df = df.loc[:, useful_datas]
    return df


def csv_to_dataframe(filename, useful_datas=None, sep=','):
    """
        converts a csv file into a pandas.dataframe

        Parameters
        ----------
        filename : str, path to csv file

        useful_datas : [str] of the columns we want to keep in the pandas.dataframe,
                       default = None (all are kept)

        sep : what separates the tweets in the csv file, default = ','

        Returns
        -------
        df : pandas.dataframe of given data

    """
    df = pd.read_csv(filename, sep=sep)
    if useful_datas is not None:
        df = df.loc[:, useful_datas]
    return df
