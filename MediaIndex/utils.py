import configparser
import json

import exiftool
import get_files
import redis
import rq
import xxhash
import os

cfg_dir = os.path.dirname(os.path.abspath(__file__))
cfg = os.path.join(cfg_dir, "config.ini")

config = configparser.ConfigParser()
config.read(cfg)

exif_cache = redis.StrictRedis(host=config["redis"]["host"], port=config["redis"]["port"], db=config["redis"]["exif"])
xxhash_cache = redis.StrictRedis(host=config["redis"]["host"], port=config["redis"]["port"], db=config["redis"]["xxhash"])

r = redis.StrictRedis(host=config["redis"]["host"], port=config["redis"]["port"], db=config["redis"]["rq"])
q = rq.Queue(connection=r)


def get_str_xxhash(string=""):
    """Return the xxhash of a given string."""
    x = xxhash.xxh64()
    x.update(string)
    return x.hexdigest()


def get_xxhash(fname):
    """ Get the xxhash of a given file."""
    hash64 = xxhash.xxh64()
    with open(str(fname), "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash64.update(chunk)
    return hash64.hexdigest()


def get_exif(fname):
    """Get the exif of a given file."""
    with exiftool.ExifTool() as et:
        return et.get_metadata(str(fname))


def cache_xxhash(media_file):
    """Return the xxhash of a given media file. Cache if it is not already cached."""
    XXHASH_ = xxhash_cache.get(str(media_file))
    if XXHASH_ is None:
        XXHASH = get_xxhash(str(media_file))
        xxhash_cache.set(str(media_file), XXHASH)
        print("Caching hash: {}".format(media_file))
    else:
        XXHASH = XXHASH_.decode()
        print("Cached hash : {}".format(media_file))
    return XXHASH


def cache_exif(media_file):
    XXHASH_ = cache_xxhash(media_file)
    EXIF_ = exif_cache.get(XXHASH_)
    if EXIF_ is None:
        EXIF = get_exif(media_file)
        exif_cache.set(XXHASH_, json.dumps(EXIF))
        print("Caching EXIF: {}".format(media_file))
    else:
        EXIF = json.loads(EXIF_.decode())
        print("Cached EXIF : {}".format(media_file))
    return EXIF


def scan_dir(root_dir):
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
        q.enqueue(scan_dir, media_dir)
    # Scan given directory for files, to a depth of 1
    media_files = get_files.get_files(root_dir, depth=1)
    # For each media_file:
    for media_file in media_files:
        # Queue scanning the media's exif data.
        q.enqueue(cache_exif, media_file)
