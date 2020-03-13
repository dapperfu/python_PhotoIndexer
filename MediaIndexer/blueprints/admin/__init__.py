import json

from jinja2 import TemplateNotFound

from flask import abort
from flask import Blueprint
from flask import render_template

admin = Blueprint(
    "admin", __name__, template_folder="templates", url_prefix="/admin"
)


@admin.route("/")
def index():
    return "Hello Admin"
