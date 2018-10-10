#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""

import MediaIndexer
from MediaIndexer import redis_cache
from .redis_utils import load_databases
import rq
import uuid

def get_connection(config_file, database):
    databases = load_databases(config_file)
    return databases[database]

def get_queue(**kwargs):
    connection = get_connection(**kwargs)
    return rq.Queue(connection=connection)

def get_worker(**kwargs):
    connection = get_connection(**kwargs)
    return rq.Worker("default", connection=connection)

def cache_dir(self, root_dir):
    # Scan for directories in the given root directory, to a depth of 1
    media_dirs = get_files.get_dirs(root_dir, depth=1)
    # For each found directory:
    for media_dir in media_dirs:
        # Don't scan zfs snap directories
        if ".zfs" in media_dir:
            continue
        # Don't follow symbolic links.
        if os.path.islink(media_dir):
            continue
        # Queue scanning the folder.
        self.queue.enqueue(cache_dir, media_dir)
    # Scan given directory for files, to a depth of 1
    media_files = get_files.get_files(root_dir, depth=1)
    # For each media_file:
    for media_file in media_files:
        # Queue scanning the media's exif data.
        self.queue.enqueue(self.cache_thumbnail, media_file)
