# -*- coding: utf-8 -*-
"""MediaIndexer 
"""

import os
import rq
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
    click.echo('Hello {}!'.format(m))
    connection = m.databases["rq"]
    w = rq.Worker("default", connection=connection)

    w.work()    m = MediaIndexer.MediaIndexer(config)



