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


if __name__ == "__main__":
    w = rq.Worker("default", connection=r)
    w.work()
