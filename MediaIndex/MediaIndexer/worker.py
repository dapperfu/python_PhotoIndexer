#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""

from . import redis_utils
from . import redis_cache
from . import rq_utils
import os

def cache_xxhash(file_path):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    database = os.environ["MEDIAINDEXER_DB"]
    databases = redis_utils.load_databases(config_file)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_xxhash(**cfg)

def cache_exif(file_path):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = redis_utils.load_databases(config_file)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_exif(**cfg)

def cache_thumbnail(file_path):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = redis_utils.load_databases(config_file)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_thumbnail(**cfg)

def scan_dir(directory):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    database = os.environ["MEDIAINDEXER_DB"]
    queue = rq_utils.get_queue(config_file=config_file, database=database)

    databases = redis_utils.load_databases(config_file)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_thumbnail(**cfg)
