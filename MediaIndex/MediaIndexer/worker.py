#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""."""

import MediaIndex

def work(**kwargs):
    w = rq.Worker("default", **kwargs)
    w.work()
    