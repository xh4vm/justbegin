from flask import Blueprint

from .routes import Chats


bp = Blueprint('chats', __name__, url_prefix='/chats')

Chats.register(bp, route_base='/')
