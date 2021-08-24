from flask import Blueprint

from .routes import Users
from .auth.routes import Auth
from .account.routes import Account


bp = Blueprint('users', __name__, url_prefix='/users')

Users.register(bp, route_base='/')
Auth.register(bp, route_base='/auth/')
Account.register(bp, route_base='/account/')
