from app.utils.request_type.JSON import JSON
from sqlalchemy.orm.scoping import scoped_session
from .methods import IAuth
from datetime import datetime
from werkzeug.exceptions import NotFound
from app import db
from app.decorators import request_validation_required
from flask import jsonify, redirect, current_app
from flask_classy import FlaskView, route
from .exceptions import AuthExceptions
from ..decorators import already_auth
from app.user.models import User
from .utils import get_auth_instance
from .schemas import post_user_schema, put_user_schema, post_reset_schema, put_reset_schema
import jwt


class Auth(FlaskView):
    session: scoped_session = db.session

    @route('/sign_in/', methods=["POST"])
    @request_validation_required(post_user_schema)
    @already_auth(response=AuthExceptions.ALREADY_AUTH, code=208)
    def sign_in(self, validated_request : dict):
        instance : IAuth = get_auth_instance()
        return instance.sign_in(email=validated_request.get("email"), password=validated_request.get("password"))

    @route('/sign_up/', methods=["POST"])
    @request_validation_required(put_user_schema, JSON)
    @already_auth(response=AuthExceptions.ALREADY_AUTH, code=208)
    def sign_up(self, validated_request : dict):
        data : dict = {
            'first_name': validated_request.get('first_name'),
            'last_name': validated_request.get('last_name'),
            'email': validated_request.get('email'),
            'nickname': validated_request.get('nickname'),
            'password': validated_request.get('password'),
            'confirm_password': validated_request.get('confirm_password'),
            'avatar': validated_request.get('avatar'),
            'telegram_nickname': validated_request.get('telegram_nickname')
        }
        instance : IAuth = get_auth_instance()

        return instance.sign_up(data=data)

    @route('/reset/', methods=["POST"])
    @request_validation_required(post_reset_schema)
    @already_auth(response=AuthExceptions.ALREADY_AUTH, code=208)
    def reset_password(self, validated_request : dict):
        instance : IAuth = get_auth_instance()
        return instance.reset_password(email=validated_request.get('email'))

    @route('/reset/<token>/', methods=["PUT"])
    @request_validation_required(put_reset_schema)
    @already_auth(response=AuthExceptions.ALREADY_AUTH, code=208)
    def reset_password_view(self, token: str, validated_request : dict):
        try:
            token_data : dict = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], 
                algorithms=[current_app.config['JWT_ALGORITHM']])
        except:
            return jsonify(AuthExceptions.RESET_TOKENT_EXPIRED), 408

        if datetime.now().timestamp().__int__() > token_data['exp']:
            return jsonify(AuthExceptions.RESET_TOKENT_EXPIRED), 408

        password : str = validated_request.get('password')
        user : User = User.query.with_entities(User)\
            .filter_by(id=token_data['id'], email=token_data['email']).first()

        if password is None or user is None:
            return jsonify(AuthExceptions.BAD_AUTH_DATA), 400

        user.password = User.create_password_hash(password)
        self.session.commit()

        return "", 200

    @route('/logout/', methods=['GET'])
    def logout(self):
        instance : IAuth = get_auth_instance()
        return instance.logout()


