from flask import Blueprint

bp = Blueprint('main', __name__)

from app.home import routes