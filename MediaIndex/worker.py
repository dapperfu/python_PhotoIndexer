#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""worker module utils.

Usage:
  worker.py
  worker.py <queue>

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
import configparser
import os
import sys

from docopt import docopt
import redis
import rq
import redis_db

def work(**kwargs):
    w = rq.Worker("default", **kwargs)
    w.work()


if __name__ == "__main__":
    arguments = docopt(__doc__, version="redis_db.py 0.1")
    print(arguments)

    if arguments["<queue>"] is None:
        db_ = "rq"
    else:
        db_ = "rq_{}".format(arguments["<queue>"])

    connection = redis_db.databases[db_]
    print("Connection: {}".format(connection))
    work(connection=connection)



