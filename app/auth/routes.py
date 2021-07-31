from datetime import datetime
from re import A
from flask_jwt_extended.view_decorators import jwt_required
from app import db
from app import auth
from app.auth import methods
from app.decorators import already_auth, request_is_json
from flask import json, render_template, request, jsonify, redirect, current_app
from flask_jwt_extended import create_access_token, jwt_optional, get_jwt_identity, set_access_cookies
from flask_classy import FlaskView, route
from app.auth import bp
from app.auth.methods.Authentificator import Authentificator
from app.auth.responses import *
from app.models import User
import importlib
import jwt


class Auth(FlaskView):

    @jwt_optional
    def get(self):
        if get_jwt_identity() is not None:
            return redirect('/', code=303)

        return render_template('auth/index.html'), 200

    @route("", methods=[])
    def get_auth_instance(self):
        auth_methods_module = importlib.import_module("app.auth.methods."+current_app.config["AUTH_METHOD"])
        auth_method = getattr(auth_methods_module, current_app.config["AUTH_METHOD"])

        auth_method = Authentificator(auth_method)
        return auth_method.get_instance()

    @route('/sign_in/', methods=["POST"])
    @jwt_optional
    @request_is_json(error_message=AuthResponses.BAD_DATA_TYPE, error_code=400)
    def sign_in(self):
        email = request.json.get("email")
        password = request.json.get("password")
        instance = self.get_auth_instance()

        return instance.sign_in(email=email, password=password)

    @route('/sign_up/', methods=["POST"])
    @jwt_optional
    @request_is_json(error_message=AuthResponses.BAD_DATA_TYPE, error_code=400)
    @already_auth(response=AuthResponses.ALREADY_AUTH, code=208)
    def sign_up(self):
        data = request.json
        instance = self.get_auth_instance()

        return instance.sign_up(data=data)

    @route('/reset/', methods=["POST"])
    @jwt_optional       
    @request_is_json(error_message=AuthResponses.BAD_DATA_TYPE, error_code=400)
    @already_auth(response=AuthResponses.ALREADY_AUTH, code=208)
    def reset_password(self):
        email = request.json.get("email")
        instance = self.get_auth_instance()

        return instance.reset_password(email=email)

    @route('/reset/<token>/', methods=["GET", "POST"])
    
    @jwt_optional       
    @already_auth(response=AuthResponses.ALREADY_AUTH, code=208)
    def reset_password_view(self, token: str):
        token_data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])

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

    @jwt_required
    @route('/logout/', methods=['GET'])
    def logout(self):
        instance = self.get_auth_instance()
        return instance.logout()


Auth.register(bp)
