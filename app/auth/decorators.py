from functools import wraps

from flask import jsonify, abort

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

        kwargs['user_id'] = get_auth_instance().get_current_user_data_from_token()[0]

        return f(*args, **kwargs)
    return decorated_function
