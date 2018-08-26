import configparser
import os

import redis
import rq

cfg_dir = os.path.dirname(os.path.abspath(__file__))
cfg = os.path.join(cfg_dir, "config.ini")

config = configparser.ConfigParser()
config.read(cfg)

r = redis.StrictRedis(
    host=config["redis"]["host"],
    port=config["redis"]["port"],
    db=config["redis"]["rq"],
)



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


if __name__ == "__main__":
    w = rq.Worker("default", connection=r)
    w.work()
