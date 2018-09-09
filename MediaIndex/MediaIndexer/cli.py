# -*- coding: utf-8 -*-
"""Module for the ```darknet.py``` command line interface.

An entrypoint for ```pydarknet2``` module.
"""

import os

import click

import MediaIndexer

from .config import config
from .utils import url_is_alive


@click.group()
@click.version_option()
def cli():
    """```pydarknet2``` command line interface entry point.

    darknet.py is a utility for interacting with pydarknet from the
    command line.
    """

