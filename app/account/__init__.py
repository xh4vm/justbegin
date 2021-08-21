from flask import Blueprint
from .routes import Account

bp = Blueprint('account', __name__, url_prefix='/account')

Account.register(bp, route_base='/')
