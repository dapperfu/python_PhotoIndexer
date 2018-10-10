#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""

import sys
from docopt import docopt
import redis_db
import rq
import redis_cache
import get_files
import os




def foo(root_dir, *args, **kwargs):
    print("Barr: {}".format(root_dir))

if __name__ == "__main__":
    arguments = docopt(__doc__, version="redis_db.py 0.1")
    print(arguments)


    redis_cache.cache_dir(arguments["<path>"])
