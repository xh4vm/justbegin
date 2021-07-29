from app import db
from app import auth
from app.auth import methods
from app.decorators import already_auth, request_is_json
from flask import render_template, request, jsonify, redirect, current_app
from flask_jwt_extended import create_access_token, jwt_optional, get_jwt_identity, set_access_cookies
from flask_classy import FlaskView, route
from app.auth import bp
from app.auth.methods.Authentificator import Authentificator
from app.auth.responses import *
import importlib


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
    def reset_password(self):
        pass

Auth.register(bp)
