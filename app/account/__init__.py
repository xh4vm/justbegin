from flask import Blueprint
from .routes import Account


bp = Blueprint('account', __name__)

Account.register(bp)
