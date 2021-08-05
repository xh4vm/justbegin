from functools import wraps
from flask import redirect, jsonify, request
from app.auth.utils import get_auth_instance


def request_is_json(error_message: str, error_code: int):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify(error_message), error_code
            return f(*args, **kwargs)
        return decorated_function
    return decorator

