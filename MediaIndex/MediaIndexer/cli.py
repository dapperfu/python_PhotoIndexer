# -*- coding: utf-8 -*-
"""MediaIndexer
"""

import os
import rq
import click
import click_config_file
from . import worker
from .redis_utils import load_databases
from .rq_utils import get_queue, get_worker, get_connection
from . import queue_tasks

import configparser

@click.group()
@click.version_option()
def cli():
    """MediaIndexer command line interface entry point.

    """

@cli.command()
@click.argument("config", type=click.Path(exists=True, resolve_path=True))
@click.option('--cfg_db', default="rq", show_default=True, type=str)
def worker(config, cfg_db):
    w = get_worker(config_file=config, database=cfg_db)
    w.work()

@cli.command()
@click.argument("config", type=click.Path(exists=True, resolve_path=True))
@click.option('--cfg_db', default="rq", show_default=True, type=str)
def test(**kwargs):
    for key, value in kwargs.items():
        print("{}: {}".format(key, value))
