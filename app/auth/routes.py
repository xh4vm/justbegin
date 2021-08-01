from datetime import datetime
from werkzeug.exceptions import NotFound
from app import db
from app.decorators import request_is_json
from app.auth.decorators import already_auth
from flask import json, render_template, request, jsonify, redirect, current_app
from flask_classy import FlaskView, route
from app.auth import bp
from app.auth.responses import *
from app.models import User
from app.auth.utils import get_auth_instance
import jwt


class Auth(FlaskView):

    def get(self):
        instance = get_auth_instance()
        return instance.get(template='auth/index.html')

    @route('/sign_in/', methods=["POST"])
    @request_is_json(error_message=AuthResponses.BAD_DATA_TYPE, error_code=400)
    @already_auth(response=AuthResponses.ALREADY_AUTH, code=208)
    def sign_in(self):
        email = request.json.get("email")
        password = request.json.get("password")
        instance = get_auth_instance()

        return instance.sign_in(email=email, password=password)

    @route('/sign_up/', methods=["POST"])
    @request_is_json(error_message=AuthResponses.BAD_DATA_TYPE, error_code=400)
    @already_auth(response=AuthResponses.ALREADY_AUTH, code=208)
    def sign_up(self):
        data = request.json
        instance = get_auth_instance()

        return instance.sign_up(data=data)

    @route('/reset/', methods=["POST"])
    @request_is_json(error_message=AuthResponses.BAD_DATA_TYPE, error_code=400)
    @already_auth(response=AuthResponses.ALREADY_AUTH, code=208)
    def reset_password(self):
        email = request.json.get("email")
        instance = get_auth_instance()

        return instance.reset_password(email=email)

    @route('/reset/<token>/', methods=["GET", "POST"])
    @already_auth(response=AuthResponses.ALREADY_AUTH, code=208)
    def reset_password_view(self, token: str):
        try:
            token_data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=[current_app.config['JWT_ALGORITHM']])
        except:
            return jsonify(AuthResponses.RESET_TOKENT_EXPIRED), 408

        if datetime.now().timestamp().__int__() > token_data['exp']:
            return jsonify(AuthResponses.RESET_TOKENT_EXPIRED), 408

        # Рендеринг страницы с вводом нового пароля
        if request.method == "GET":
            pass

        password = request.json.get('password')
        user = User.query.with_entities(User).filter_by(id=token_data['id'], email=token_data['email']).first()

        if password is None or user is None:
            return jsonify(AuthResponses.BAD_AUTH_DATA), 400

        user.password = User.create_password_hash(password)
        db.session.commit()

        return jsonify(AuthResponses.RESET_PASSWORD_SUCCESS), 200

    @route('/logout/', methods=['GET'])
    def logout(self):
        instance = get_auth_instance()
        return instance.logout()

    # @route("/refresh/", methods=["POST"])
    # def refresh():
    #     if current_app.config['AUTH_METHOD'] != 'JWTAuth':
    #         return NotFound, 404
        
    #     instance = get_auth_instance()
    #     return instance.refresh()



Auth.register(bp)
