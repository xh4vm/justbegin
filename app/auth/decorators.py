from functools import wraps

from flask import jsonify, abort

from .utils import get_auth_instance
from ..models import User


def already_auth(response: str, code: int):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            instance = get_auth_instance()
            if instance.already_auth():
                return jsonify(response), code
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def check_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        instance = get_auth_instance()
        if not instance.already_auth():
            abort(401)
        return f(*args, **kwargs)
    return decorated_function


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = get_auth_instance()

        if not auth.already_auth():
            abort(401)

        user_id = auth.get_current_user_data_from_token()[0]
        user = User.query.get(user_id)

        if user is None:
            abort(500)

        kwargs['user'] = user

        return f(*args, **kwargs)
    return decorated_function
