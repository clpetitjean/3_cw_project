"""Tests propagatweet.utils.conversion """
import pandas
from propagatweet.utils.conversion import *
from propagatweet.env import *


def test_json_to_dataframe():
    """
        function that tests the function json_to_dataframe():
            must return a dataframe with at least the 'full_text' column

    """
    df = json_to_dataframe(PATH_DATA_JSON, useful_datas=['full_text'])
    assert 'full_text' in df.columns


def test_csv_to_dataframe():
    """
        function that tests the function csv_to_dataframe():
            must return a dataframe

    """
    df = csv_to_dataframe(PATH_DATASET_TRAIN)
    assert type(df) == pandas.core.frame.DataFrame
