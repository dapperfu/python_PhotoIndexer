#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""

import MediaIndexer
from MediaIndexer import redis_cache

def cache_xxhash(config, file_path):
    databases = MediaIndexer.redis_db.load_databases(config)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_xxhash(**cfg)

def cache_exif(config, file_path):
    databases = MediaIndexer.redis_db.load_databases(config)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_exif(**cfg)

def cache_thumbnail(config, file_path):
    databases = MediaIndexer.redis_db.load_databases(config)
    cfg = {
        "file_path": file_path,
        "databases": databases,
    }
    redis_cache._get_thumbnail(**cfg)
