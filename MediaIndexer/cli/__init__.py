"""MediaIndexer command line interface.
"""
import os
import time

import click
import MediaIndexer.flask
import MediaIndexer.worker
from MediaIndexer.redis_utils import load_databases
from MediaIndexer.rq_utils import get_queue
from MediaIndexer.rq_utils import get_worker
from prettytable import PrettyTable

from .__init__ import __version__

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels

class Info:
    """
    An information object to pass data between CLI functions.
    """

    def __init__(self):  # Note: This object must have an empty constructor.
        self.verbose: int = 0


@click.group()
@click.version_option()
@click.option(
    "--config",
    envvar="MEDIAINDEXER_CFG",
    default="config.ini",
    show_default=True,
    type=click.Path(exists=True, resolve_path=True),
)
@click.option(
    "--queue_db", envvar="MEDIAINDEXER_DB", default="rq", show_default=True
)
def cli(config, queue_db):
    """MediaIndexer command line interface.

    """
    os.environ["MEDIAINDEXER_CFG"] = config
    os.environ["MEDIAINDEXER_DB"] = queue_db


@cli.command()
def worker():
    """Launch MediaIndexer worker.

Launch a worker instance."""
    queue_db = os.environ["MEDIAINDEXER_DB"]
    config = os.environ["MEDIAINDEXER_CFG"]
    w = get_worker(config_file=config, database=queue_db)
    w.work()


@cli.command()
@click.option("--fcn", default="cache_face_encodings", show_default=True)
@click.argument(
    "dirs",
    nargs=-1,
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
)
def scan(**kwargs):
    """Use MediaIndexer to scan a directory."""
    queue_db = os.environ["MEDIAINDEXER_DB"]
    config = os.environ["MEDIAINDEXER_CFG"]
    fcn = kwargs["fcn"]
    queue = get_queue(config_file=config, database=queue_db)
    for d in kwargs["dirs"]:
        queue.enqueue(MediaIndexer.worker.scan_dir, d, fcn)


@cli.command()
@click.option("--host", default="0.0.0.0", show_default=True, type=str)
def server(**kwargs):
    """Launch MediaIndexer Flask server."""
    app = MediaIndexer.flask.create_app()
    app = MediaIndexer.flask.update_blueprints(app)
    app.config["CONFIG"] = os.environ["MEDIAINDEXER_CFG"]
    app.run(debug=True, host=kwargs["host"])


@cli.group("redis")
def db(**kwargs):
    """Manage MediaIndexer redis databases.
    """


@db.command("keys")
def keys(**kwargs):
    """Print number of keys in the redis database."""
    databases = load_databases(os.environ["MEDIAINDEXER_CFG"])
    tbl = PrettyTable()
    tbl.field_names = ["Redis DB", "Keys"]
    for db_name, database in databases.items():
        tbl.add_row([db_name, database.dbsize()])
    print(tbl)


def callback(ctx, param, value):
    if not value:
        ctx.abort()


@db.command("flush")
@click.option(
    "--yes",
    is_flag=True,
    callback=callback,
    expose_value=False,
    prompt="Are you sure you want to flush all redis databases?",
)
def dropdb(**kwargs):
    """Flush all data from the redis database."""
    databases = load_databases(os.environ["MEDIAINDEXER_CFG"])
    for db_name, database in databases.items():
        print(f"Flushing: {db_name}...", end="")
        t1 = time.time()
        database.flushdb()
        t2 = time.time()
        print("...done ({:.1f})".format(t2 - t1))
