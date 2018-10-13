from flask import Blueprint, render_template, abort, url_for
from jinja2 import TemplateNotFound
import json
import os
import get_files
import tempfile
# from w3c_validator import validate
from MediaIndexer.redis_cache import _get_xxhash
import MediaIndexer.redis_utils

#config_file = os.environ["MEDIAINDEXER_CFG"]
#databases = MediaIndexer.redis_utils.load_databases(config_file)

gallery = Blueprint(
    name='gallery',
    import_name=__name__,
    static_folder='static',
    static_url_path='/static',
    template_folder='templates',
    url_prefix='/gallery'
)

@gallery.route('/', defaults={'page': ''})
@gallery.route('/<page>')
def index(**kwargs):
    for i, (key, value) in enumerate(kwargs.items()):
        print("[{}] {}: {}".format(i, key, value))

    root=os.path.abspath(os.curdir)
    if not os.path.exists(root):
        abort(404)
    path = os.path.abspath(os.path.join(root, kwargs["page"]))
    if not os.path.exists(path):
        abort(404)
    directories_ = get_files.get_dirs(directory = path, depth=1, absolute=True)
    directories = [directory.replace(root, "").strip(os.path.sep) for directory in directories_]
    images_ = get_files.get_files(directory = path, extensions=['.jpg'], depth=1, absolute=True)

    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = MediaIndexer.redis_utils.load_databases(config_file)

    images = list()
    for image_ in images_:
        images.append({
            "xxhash": _get_xxhash(file_path=image_, databases=databases)
        })

    for key, item in kwargs.items():
        print("{}: {}".format(key, item))
    html = render_template('index.html', directories=directories, images=images, sizes=[128, 608, 2048])


    """
    with tempfile.NamedTemporaryFile(mode="w", delete=True) as f:
        f.write(html)
        f.flush()
        print(validate(f.name))
    """
    return html

@gallery.route('/items.json', defaults={'page': ''})
@gallery.route('/<page>/items.json')
def items(**kwargs):
    r = os.path.abspath(os.path.join(os.curdir, kwargs["page"]))
    directories = get_files.get_dirs(directory = r, depth=1, absolute=True)
    images = get_files.get_files(directory = r, extensions=['.jpg'], depth=1, absolute=True)
    for key, item in kwargs.items():
        print("{}: {}".format(key, item))
    items_json = render_template('items.json', directorys=directories, images=images)
    return items_json

import json
@gallery.route('/items2.json', defaults={'page': ''})
@gallery.route('/<page>/items2.json')
def items2(**kwargs):
    sizes = {
        "mediumImage": 128,
        "originalImage": 608,
    }

    config_file = os.environ["MEDIAINDEXER_CFG"]
    databases = MediaIndexer.redis_utils.load_databases(config_file)

    items=list()

    root=os.path.join(os.curdir)
    path = os.path.abspath(os.path.join(os.curdir, kwargs["page"]))
    directories = get_files.get_dirs(directory = path, depth=1, absolute=True)
    images = get_files.get_files(directory = path, extensions=['.jpg'], depth=1, absolute=True)

    for image in images:
        item = {
            "xxhash": _get_xxhash(file_path=image, databases=databases),
        }
        for size_name, size in sizes.items():
            item[size_name] = url_for("thumbnails.get_thumbnail", size=size, xxhash=item["xxhash"])

        items.append(item)

    items_ = {
        "items": items,
    }
    return json.dumps(items_)

@gallery.route('/style.css')
def css(**kwargs):
    for key, item in kwargs.items():
        print("{}: {}".format(key, item))
    return render_template('style.css')


@gallery.route('/hello')
@gallery.route('/hello/')
def hello(**kwargs):
    for key, item in kwargs.items():
        print("{}: {}".format(key, item))
    return render_template('index.html')

