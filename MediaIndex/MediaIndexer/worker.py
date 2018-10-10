#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""

import MediaIndexer
from MediaIndexer import redis_cache

def cache_xxhash(config_file, file_path):
    databases = MediaIndexer.redis_db.load_databases(config_file)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_xxhash(**cfg)

def cache_exif(config_file, file_path):
    databases = MediaIndexer.redis_db.load_databases(config_file)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_exif(**cfg)

def cache_thumbnail(config_file, file_path):
    databases = MediaIndexer.redis_db.load_databases(config_file)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_thumbnail(**cfg)
