"""MediaIndexer utilities module.

Generic utilities for use in MediaIndexer.
"""
import configparser
import copy
import io

import numpy as np


def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def arr_to_bytes(arr) -> bytes:
    """ Convert a numpy array to a bytestring containing a saved numpy file.

    Purpose: Numpy arrays in redis & databases.
    """
    with io.BytesIO() as b:
        np.save(b, arr, allow_pickle=False, fix_imports=False)
        serialized_arr = copy.deepcopy(b.getvalue())
    return serialized_arr


def bytes_to_arr(array_bytes):
    """" Convert a bytestring into a numpy array. """
    return np.load(copy.deepcopy(io.BytesIO(array_bytes)))
