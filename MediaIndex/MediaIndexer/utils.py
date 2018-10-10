# -*- coding: utf-8 -*-
"""MediaIndexer utilities module.

Generic utilities for use in MediaIndexer.
"""

import io
import configparser
from PIL import Image

def pil_thumbnail(thumbnail_str):
    assert isinstance(thumbnail_str, bytes)
    return Image.open(io.BytesIO(thumbnail_str))


def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config
