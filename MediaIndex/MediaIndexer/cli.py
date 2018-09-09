# -*- coding: utf-8 -*-
"""MediaIndexer 
"""

import os

import click

from .config import config


@click.group()
@click.version_option()
@click.option('--name', default='World', help='Who to greet.')
@click_config_file.configuration_option()
def hello(name):
    click.echo('Hello {}!'.format(name))

