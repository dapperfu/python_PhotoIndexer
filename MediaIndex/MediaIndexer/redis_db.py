#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""redis_db module utils.

Usage:
  redis_db.py
  redis_db.py flush

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
import configparser
import os
import sys

import redis

def load_databases(cfg="config.ini"):

    config = configparser.ConfigParser()
    config.read(cfg)
    
    databases = dict()
    for key in config["redis"].keys():
        if key in ["host", "port"]:
            continue
        db_ = redis.StrictRedis(
            host=config["redis"]["host"],
            port=config["redis"]["port"],
            db=config["redis"][key],
        )
        databases[key] = db_
    return databases