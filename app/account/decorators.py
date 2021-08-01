from functools import wraps
from flask import jsonify, redirect
from app.auth.utils import get_auth_instance

def check_auth():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            instance = get_auth_instance()
            if not instance.already_auth():
                return redirect('/auth', code=302)
            return f(*args, **kwargs)
        return decorated_function
    return decorator