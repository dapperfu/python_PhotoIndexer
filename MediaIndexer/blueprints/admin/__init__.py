import json

from flask import abort
from flask import Blueprint
from flask import render_template
from jinja2 import TemplateNotFound

admin = Blueprint(
    "admin", __name__, template_folder="templates", url_prefix="/admin"
)


@admin.route("/")
def index():
    return "Hello Admin"
