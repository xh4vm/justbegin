from flask import Blueprint
from .routes import Auth


bp = Blueprint('auth', __name__, url_prefix='/auth')

Auth.register(bp, route_base='/')