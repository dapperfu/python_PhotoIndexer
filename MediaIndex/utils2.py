import configparser
import json

import exiftool
import get_files
import redis
import rq
import xxhash

config = configparser.ConfigParser()
config.read("config.ini")

r = redis.StrictRedis(
    host=config["redis"]["host"],
    port=config["redis"]["port"],
    db=1,
)
q = rq.Queue(connection=r)

