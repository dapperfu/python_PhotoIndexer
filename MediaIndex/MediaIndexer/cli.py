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
import MediaIndexer.worker
import MediaIndexer.flask

import configparser

@click.group()
@click.version_option()
def cli():
    """MediaIndexer command line interface entry point.

    """

@cli.command()
@click.option("--config", default="config.ini", show_default=True, type=click.Path(exists=True, resolve_path=True))
@click.option('--cfg_db', default="rq", show_default=True, type=str)
def worker(config, cfg_db):
    os.environ["MEDIAINDEXER_CFG"]=config
    os.environ["MEDIAINDEXER_DB"]=cfg_db
    w = get_worker(config_file=config, database=cfg_db)
    w.work()

@cli.command()
@click.option("--config", default="config.ini", show_default=True, type=click.Path(exists=True, resolve_path=True))
@click.option('--cfg_db', default="rq", show_default=True, type=str)
@click.argument('dirs', nargs=-1, type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=False, readable=True, resolve_path=True))
def scan(**kwargs):
    os.environ["MEDIAINDEXER_CFG"]=kwargs["config"]
    os.environ["MEDIAINDEXER_DB"]=kwargs["cfg_db"]

    queue = get_queue(config_file = kwargs["config"], database = kwargs["cfg_db"])
    for d in kwargs["dirs"]:
        queue.enqueue(MediaIndexer.worker.scan_dir, d)

@cli.command()
@click.option("--config", default="config.ini", show_default=True, type=click.Path(exists=True, resolve_path=True))
@click.option('--cfg_db', default="rq", show_default=True, type=str)
@click.option('--host', default="0.0.0.0", show_default=True, type=str)
def server(**kwargs):
    os.environ["MEDIAINDEXER_CFG"]=kwargs["config"]
    os.environ["MEDIAINDEXER_DB"]=kwargs["cfg_db"]
    app = MediaIndexer.flask.create_app()
    app = MediaIndexer.flask.update_blueprints(app)
    app.run(debug=True, host=kwargs["host"])


@cli.command()
def test(**kwargs):
    # queue = MediaIndexer.rq_utils.get_queue(config_file=config_file, database="rq")
    # queue.enqueue(MediaIndexer.worker.scan_dir, "/net/nas.local/mnt/keg/Pictures")
    for key, value in kwargs.items():
        print("{}: {}".format(key, value))
