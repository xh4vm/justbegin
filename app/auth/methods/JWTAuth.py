from flask import make_response, jsonify, redirect
from app import db
from app.models import User
from app.auth.responses import AuthResponses
from flask_jwt_extended import create_access_token, set_access_cookies
from app.auth.methods import IAuth


class JWTAuth(IAuth):
    def sign_in(self, email, password):
        user = User.query.with_entities(User).filter_by(email=email).first()

        if user is None or not user.check_password(password):
            return jsonify(AuthResponses.BAD_AUTH_DATA), 400

        access_token = create_access_token(identity=user)
        response = make_response(redirect('/', code=303))

        set_access_cookies(response, access_token)

        return response

    def sign_up(self, data):
        if data.get('password') != data.get('confirm_password'):
            return jsonify(AuthResponses.BAD_CONFIRM_PASSWORD), 400

        user = User(first_name=data.get('first_name'), last_name=data.get('last_name'),
                    nickname=data.get('nickname'), email=data.get('email'), 
                    password=data.get('password'), telegram_nickname=data.get('telegram_nickname'))

        if not user.check_email():
            return jsonify(AuthResponses.DUPLICATE_EMAIL), 400

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user)
        response = make_response(redirect('/', code=303))

        set_access_cookies(response, access_token)

        return response

    def reset_password(self, email):
        pass