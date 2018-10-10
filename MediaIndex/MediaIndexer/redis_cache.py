#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""redis_db module ^ utils.

Usage:
  redis_cache.py IMAGE

Options:
  -h --help     Show this screen

"""
import json

from docopt import docopt
from MediaIndexer import utils

class RedisCacheMixin(object):
    def get_xxhash(self, file_path):
        """Return the xxhash of a given media file.
    
        Cache if it is not already cached."""
        if isinstance(file_path, bytes):
            file_path = file_path.decode("UTF-8")
        file_path = str(file_path)
    
        if redis_db.xxhash.exists(file_path):
            XXHASH = redis_db.xxhash.get(file_path).decode("UTF-8")
            print("[X] hash : {}".format(file_path))
        else:
            XXHASH = utils.get_xxhash(file_path)
            redis_db.xxhash.set(file_path, XXHASH)
            print("[ ] hash: {}".format(file_path))
        return XXHASH
    
    
    def get_exif(self, file_path):
        if isinstance(file_path, bytes):
            file_path = file_path.decode("UTF-8")
        file_path = str(file_path)
    
        file_hash = get_xxhash(file_path)
        if redis_db.exif.exists(file_hash):
            exif_ = redis_db.exif.get(file_hash)
            exif = json.loads(exif_.decode("UTF-8").replace("'", "\""))
            print("[X] EXIF : {}".format(file_path))
        else:
            exif = utils.get_exif(file_path)
            exif_ = json.dumps(exif)
            redis_db.exif.set(file_hash, exif_)
            print("[ ] EXIF: {}".format(file_path))
    
        return exif
    
    
    def get_thumbnail(self, file_path, **kwargs):
        if isinstance(file_path, bytes):
            file_path = file_path.decode("UTF-8")
        file_path = str(file_path)
    
        file_hash = get_xxhash(file_path)
    
        if redis_db.thumb.exists(file_hash):
            thumb_ = redis_db.thumb.get(file_hash)
            print("[X] thumb : {}".format(file_path))
        else:
            thumb_ = utils.get_thumbnail(file_path, pil_image=False)
            redis_db.thumb.set(file_hash, thumb_)
            print("[ ] thumb : {}".format(file_path))
    
        return thumb_
    
    def cache_xxhash(self, file_path):
        self.get_xxhash(file_path)
        return None
    
    
    def cache_exif(self, file_path):
        self.get_xxhash(file_path)
        return None
    
    def cache_thumbnail(self, file_path):
        self.get_thumbnail(file_path)
        return None

import get_files
import os
import rq

def cache_dir(root_dir):
    db_ = "rq"
    connection = redis_db.databases[db_]
    queue = rq.Queue(connection=connection)
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
        queue.enqueue(cache_dir, media_dir)
    # Scan given directory for files, to a depth of 1
    media_files = get_files.get_files(root_dir, depth=1)
    # For each media_file:
    for media_file in media_files:
        # Queue scanning the media's exif data.
        queue.enqueue(cache_thumbnail, media_file)


if __name__ == "__main__":

    arguments = docopt(__doc__, version="redis_db.py 0.1")
    print(arguments)
    file_path = arguments["IMAGE"]

    xxhash = get_xxhash(file_path)
    exif = get_exif(file_path)
    thumbnail = get_thumbnail(file_path)
    thumbnail = utils.pil_thumbnail(thumbnail)
    thumbnail.save("thumbnail.jpg")
