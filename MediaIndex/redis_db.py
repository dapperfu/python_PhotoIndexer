#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""redis_db module ^ utils.

Usage:
  redis_db.py 
  redis_db.py flush

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --yes    Drifting mine.

"""
import configparser
import os
import sys

from docopt import docopt
import redis

cfg_dir = os.path.dirname(os.path.abspath(__file__))
cfg = os.path.join(cfg_dir, "config.ini")

config = configparser.ConfigParser()
config.read(cfg)


redis_databases = dict()
for key in config["redis"].keys():
    if key in ["host", "port"]:
        continue
    db_ = redis.StrictRedis(
        host=config["redis"]["host"],
        port=config["redis"]["port"],
        db=config["redis"][key],
    )
    redis_databases[key] = db_

this = sys.modules[__name__]
for db_name, db in redis_databases.items():
    setattr(this, db_name, db)


def flush_keys():
    for db_name, db in redis_databases.items():
        print("{} db: flushing".format(db_name))


def key_count():
    for db_name, db in redis_databases.items():
        print("{} db: {} keys".format(db_name, db.dbsize()))


if __name__ == "__main__":

    arguments = docopt(__doc__, version="redis_db.py 0.1")
    print(arguments)

    if arguments["flush"] is False:
        key_count()
    else:
        flush_keys()
