from functools import wraps
from flask import redirect, jsonify, request
from flask_jwt_extended import get_jwt_identity


def request_is_json(error_message, error_code=400):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify(error_message), error_code
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def already_auth(response, code):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if get_jwt_identity() is not None:
                return jsonify(response), code
            return f(*args, **kwargs)
        return decorated_function
    return decorator
