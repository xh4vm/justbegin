from flask import redirect, request
from flask_jwt_extended import jwt_optional, get_jwt_identity
from flask_classy import FlaskView, route
from app.account import bp
from decorators import check_auth
from models import User


class Account(FlaskView):
    nickname = ""
    first_name = ""
    last_name = ""
    email = ""
    avatar_path = ""
    telegram_nickname = ""
    liked_project = []

    @jwt_optional
    @check_auth
    def get(self):
        return "Аккаунт пользователя", 200

    @check_auth
    @route("/setting")
    def set_account(self):
        if request.method == "POST":
            first_name = request.json.get("first_name")
            last_name = request.json.get("second_name")
            email = request.json.get("email")
            telegram_nickname = request.json.get("telegram_nickname")
            return redirect("/setting", 302)
        return "Настройки аккаунта", 200        


    @check_auth
    @route('/delete')
    def delete_account(self):
       pass




