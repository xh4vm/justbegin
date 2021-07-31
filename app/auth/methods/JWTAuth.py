from flask import make_response, jsonify, redirect
from flask.globals import current_app
from app import db, mail
from app.models import User
from app.auth.responses import AuthResponses
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from app.auth.methods import IAuth
from flask_mail import Message


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

        if User.contains_with_email(data.get('email')):
            return jsonify(AuthResponses.DUPLICATE_EMAIL), 400

        user = User(first_name=data.get('first_name'), last_name=data.get('last_name'),
                    nickname=data.get('nickname'), email=data.get('email'), 
                    password=data.get('password'), telegram_nickname=data.get('telegram_nickname'))

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user)
        response = make_response(redirect('/', code=303))

        set_access_cookies(response, access_token)

        return response

    def reset_password(self, email):
        if not User.contains_with_email(email):
            return jsonify(AuthResponses.UNKNOWN_USER), 400

        token = 'asd'
        msg = Message("Восстановление доступа к аккаунту", recipients=[email])
        
        msg.body = f"""
        Вами была совершена попытка сброса пароля в сервисе JustBegin!
        Если это сделали не вы, то просто проигнорируйте это сообщение. 
        В случае, если вы действительно забыли пароль, перейдите по ссылке ниже, которая активна 15 минут.

        {current_app.config['HOME_URL']}/reset/{token}
        """
        mail.send(msg)

        return jsonify(AuthResponses.TOKEN_CREATED), 201

    def logout(self):
        response = redirect('/auth/', code=303)
        unset_jwt_cookies(response)

        return response