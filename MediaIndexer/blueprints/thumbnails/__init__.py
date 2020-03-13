import json

from jinja2 import TemplateNotFound

from flask import abort
from flask import Blueprint
from flask import render_template
from flask import send_file
from flask import url_for

thumbnails = Blueprint(
    "thumbnails",
    __name__,
    template_folder="templates",
    url_prefix="/thumbnails",
)
import os
import io
import MediaIndexer.redis_utils


@thumbnails.route("/<int:size>/<string:xxhash>.jpg")
def get_thumbnail(xxhash, size=128):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = MediaIndexer.redis_utils.load_databases(config_file)

    try:
        thumbnail = MediaIndexer.redis_cache._get_thumbnail(
            file_path="", file_hash=xxhash, size=size, databases=databases
        )
        return send_file(io.BytesIO(thumbnail), mimetype="image/jpg")
    except AssertionError:
        abort(403)
    except:
        raise
