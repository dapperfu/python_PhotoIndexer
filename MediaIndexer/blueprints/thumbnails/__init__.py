from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import json

thumbnails = Blueprint('thumbnails', __name__, template_folder='templates', url_prefix='/admin')

@thumbnails.route('/')
def index():
    return "Hello Thumbnails."
