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

import redis_db
import utils


def get_xxhash(file_path):
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


def get_exif(file_path):
    if isinstance(file_path, bytes):
        file_path = file_path.decode("UTF-8")
    file_path = str(file_path)

    file_hash = get_xxhash(file_path)
    if redis_db.exif.exists(file_hash):
        exif_ = redis_db.exif.get(file_hash)
        exif = json.loads(exif_.decode("UTF-8"))
        print("[X] EXIF : {}".format(file_path))
    else:
        exif = utils.get_exif(file_path)
        exif_ = json.dumps(exif)
        redis_db.exif.exists(file_hash, exif)
        print("[ ] EXIF: {}".format(file_path))

    return exif


def get_thumbnail(file_path, **kwargs):
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


"""

"""


def cache_xxhash(file_path):
    get_xxhash(file_path)
    return None


def cache_exifsh(file_path):
    get_xxhash(file_path)
    return None


def cache_thumbnail(file_path):
    get_thumbnail(file_path)
    return None


if __name__ == "__main__":

    arguments = docopt(__doc__, version="redis_db.py 0.1")
    print(arguments)
    file_path = arguments["IMAGE"]

    xxhash = get_xxhash(file_path)
    exif = get_exif(file_path)
    thumbnail = get_thumbnail(file_path)
    thumbnail = utils.pil_thumbnail(thumbnail)
    thumbnail.save("thumbnail.jpg")
