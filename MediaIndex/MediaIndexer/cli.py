# -*- coding: utf-8 -*-
"""MediaIndexer 
"""

import os

import click
import click_config_file
from .config import config
import MediaIndexer
@click.group()
@click.version_option()
def cli():
    """MediaIndexer command line interface entry point.

    """

@cli.command()
@click.argument("config", type=click.Path(exists=True))
def worker(config):
    m = MediaIndexer.MediaIndexer(config)
    click.echo('Hello {}!'.format(m))
    connection = m.databases["rq"]
    print(connection)
    #w = rq.Worker("default", **kwargs)
    #w.work()


