#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 22:44:57 2018

@author: jed
"""
import configparser
import os
import sys

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
for key, value in redis_databases.items():
    setattr(this, key, value)

if __name__ == "__main__":
    pass
