from functools import wraps

from flask import jsonify, request
from marshmallow import Schema, ValidationError


def request_is_json(error_message: str, error_code: int):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify(error_message), error_code
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def request_validation_required(schema: Schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                validated_request = schema.load(request.form)
            except ValidationError as error:
                return jsonify({'errors': error.messages}), 400

            kwargs['validated_request'] = validated_request

            return f(*args, **kwargs)
        return decorated_function
    return decorator
