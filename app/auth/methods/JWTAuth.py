from datetime import datetime, timedelta
from flask import make_response, jsonify, redirect, render_template
from flask.globals import current_app, request
from flask_jwt_extended.utils import unset_refresh_cookies
from flask_jwt_extended.view_decorators import jwt_refresh_token_required, jwt_required, jwt_optional
from app import db, mail
from app.models import User
from app.auth.responses import AuthResponses
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt_identity
from app.auth.methods import IAuth
from flask_mail import Message
import jwt


class JWTAuth(IAuth):
    @jwt_optional
    def get(sellf, template: str) -> str:
        if get_jwt_identity() is not None:
            return redirect('/', code=303)

        return render_template(template), 200
    
    @jwt_optional
    def already_auth(self) -> bool:
        return True if get_jwt_identity() is not None else False
    
    @jwt_optional
    def sign_in(self, email: str, password: str) -> object:
        user = User.query.with_entities(User).filter_by(email=email).first()

        if user is None or not user.check_password(password):
            return jsonify(AuthResponses.BAD_AUTH_DATA), 400

        access_token = create_access_token(identity=user)
        response = make_response(redirect('/', code=303))

        set_access_cookies(response, access_token)

        return response

    @jwt_optional
    def sign_up(self, data: object) -> object:
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

    @staticmethod
    def get_token(user: User, timedelta_min=15) -> str:
        token_data = {
            "id": user.id,
            "email": user.email,
            "password": user.password,
            "exp": (datetime.now() + timedelta(minutes=timedelta_min)).timestamp().__int__()
        }
        return jwt.encode(token_data, current_app.config['JWT_SECRET_KEY'], algorithm=current_app.config['JWT_ALGORITHM']).decode()

    @jwt_optional
    def reset_password(self, email: str) -> object:
        if not User.contains_with_email(email):
            return jsonify(AuthResponses.UNKNOWN_USER), 400

        user = User.query.with_entities(User).filter_by(email=email).first()
        token = self.get_token(user)

        msg = Message("Восстановление доступа к аккаунту", recipients=[email])
        
        msg.body = f"""
        Вами была совершена попытка сброса пароля в сервисе JustBegin!
        Если это сделали не вы, то просто проигнорируйте это сообщение. 
        В случае, если вы действительно забыли пароль, перейдите по ссылке ниже, которая активна 15 минут.

        {current_app.config['HOME_URL']}/auth/reset/{token}/
        """
        mail.send(msg)

        return jsonify(AuthResponses.TOKEN_CREATED), 201

    @jwt_required
    def logout(self) -> object:
        response = redirect('/auth/', code=303)
        unset_jwt_cookies(response)

        return response

    # @jwt_refresh_token_required
    # def refresh(self):
    #     current_user = get_jwt_identity()
    #     return jsonify({'access_token': create_access_token(identity=current_user)}), 200