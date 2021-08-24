from app.utils.request_type.Form import Form
from app.utils.request_type import IRequestType
from app.user.models import User
from functools import wraps

from flask import jsonify, abort

from .auth.utils import get_auth_instance


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


def user_exists_by_email(req_type: IRequestType = Form):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            email = req_type().get().get('email')

            if User.query.filter_by(email=email).first() is None:
                abort(400)
            
            return f(*args, **kwargs)

        return decorated_function
    return decorator

def user_exists(req_type: IRequestType = Form):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = req_type().get().get('user_id')

            if User.query.get(user_id) is None:
                abort(400)
            
            return f(*args, **kwargs)

        return decorated_function
    return decorator
