"""Gives the path to a file regardless of operating system"""
from pathlib import Path
from src.env import *


def get_file_path_data(filename):
    """
        gives the path to a file regardless of operating system

        Parameters
        ----------
        filename : name of file

        Returns
        -------
        path : type = pathlib.path, path to file

    """
    file_path = (Path(PATH_DATA) / filename)
    return file_path
