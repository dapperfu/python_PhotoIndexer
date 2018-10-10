"""pydarknet configuration options.

Configuration options for all pydarknet.
"""

import configparser
import os

def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

