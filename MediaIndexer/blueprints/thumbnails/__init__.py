from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import json

thumbnails = Blueprint('thumbnails', __name__, template_folder='templates', url_prefix='/thumbnails')
import os
@thumbnails.route('/<int:size>/<string:xxhash>.jpg')
def get_thumbnail(xxhash, size=128):
    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = MediaIndexer.redis_utils.load_databases(config_file)

    thumbnail = MediaIndexer.redis_cache._get_thumbnail(
        file_path="", file_hash=xxhash, databases=databases
    )
    return send_file(io.BytesIO(thumbnail), mimetype="image/jpg")
