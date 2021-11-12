from flask import Blueprint

from .routes import Home

bp = Blueprint('main', __name__)
Home.register(bp)
