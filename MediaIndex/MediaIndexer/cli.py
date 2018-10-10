# -*- coding: utf-8 -*-
"""MediaIndexer 
"""

import os

import click
import click_config_file
from .config import config
from 

@click.group()
@click.version_option()
def cli():
    """MediaIndexer command line interface entry point.

    """

@cli.command()
@click.argument("config", type=click.Path(exists=True))
def worker(config):
    
    click.echo('Hello {}!'.format(config))

