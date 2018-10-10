# -*- coding: utf-8 -*-
"""MediaIndexer
"""

import os
import rq
import click
import click_config_file
from MediaIndexer import worker
from MediaIndexer import redis_cache

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
    databases = MediaIndexer.redis_db.load_databases(config)
    connection = databases[cfg_db]
    w = rq.Worker("default", connection=connection)
    w.work()

@cli.command()
@click.argument("config", type=click.Path(exists=True, resolve_path=True))
@click.option('--cfg_db', default="rq", show_default=True, type=str)
@click.option('--database', default=-1, show_default=True, type=int)
def test(**kwargs):
    for key, value in kwargs.items():
        print("{}: {}".format(key, value))
