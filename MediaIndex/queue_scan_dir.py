#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recursively start scanning a root directory.
"""

import sys

import utils

for import_dir in sys.argv[1:]:
    print(import_dir)
#    j = q.enqueue(utils.scan_dir, )
