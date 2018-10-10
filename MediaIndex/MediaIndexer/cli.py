# -*- coding: utf-8 -*-
"""MediaIndexer
"""

import configparser
import os
import time

import click
import click_config_file
from prettytable import PrettyTable
import rq

import MediaIndexer.flask
import MediaIndexer.worker

from . import worker
from .redis_utils import load_databases
from .rq_utils import get_connection, get_queue, get_worker


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
    app.config["CONFIG"] = kwargs["config"]
    app.run(debug=True, host=kwargs["host"])

@cli.group("db")
def db(**kwargs):
    """Manage MediaIndexer redis databases.


    """

@db.command("keys")
@click.option("--config", default="config.ini", show_default=True, type=click.Path(exists=True, resolve_path=True))
def keys(**kwargs):
    os.environ["MEDIAINDEXER_CFG"]=kwargs["config"]
    databases = load_databases(kwargs["config"])

    tbl = PrettyTable()
    tbl.field_names = ["Redis DB", "Keys"]
    for db_name, database in databases.items():
        tbl.add_row([db_name, database.dbsize()])
    print(tbl)

def callback(ctx, param, value):
        if not value:
            ctx.abort()


@db.command("flush")
@click.option("--config", default="config.ini", show_default=True, type=click.Path(exists=True, resolve_path=True))
@click.option('--yes', is_flag=True, callback=callback,
              expose_value=False, prompt='Are you sure you want to flush all redis databases?')
def dropdb(**kwargs):
    databases = load_databases(kwargs["config"])
    for db_name, database in databases.items():
        print("Flushing: {}...".format(db_name), end="")
        t1=time.time()
        database.flushdb()
        t2=time.time()
        print("...done ({:.1f})".format(t2-t1))
