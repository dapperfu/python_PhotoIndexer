from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import json

gallery = Blueprint(
    name='gallery',
    import_name=__name__,
    static_folder='static',
    static_url_path='/static',
    template_folder='templates',
    url_prefix='/gallery'
)

@gallery.route('/', defaults={'page': 'index'})
@gallery.route('/<page>')
def index(**kwargs):
    for key, item in kwargs.items():
        print("{}: {}".format(key, item))
    return json.dumps(kwargs)
