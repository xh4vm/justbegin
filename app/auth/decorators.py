from functools import wraps
from flask import jsonify
from app.auth.utils import get_auth_instance


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