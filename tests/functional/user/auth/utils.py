from app.user.auth.utils import get_auth_instance
import json
from tests.functional.header import Header
from app.db import db
from app.user.models import User
from tests.utils import random_string


def create_user(nickname: str = None, email: str = None, password: str = None, telegram_nickname: str = None) -> User:
    user = User(
        nickname or random_string(),
        email or random_string() + '@test.py',
        password or random_string(),
        telegram_nickname or random_string(),
    )

    db.session.add(user)
    db.session.commit()

    return user


def sign_in(client) -> User:
    password : str = random_string()
    user : User = create_user(password=password)
    sign_in_data : dict = {'email': user.email, 'password': password}

    client.post('/users/auth/sign_in/', data=sign_in_data)

    return user


def request_sign_in(client, nickname: str = None, email: str = None, password: str = None, telegram_nickname: str = None) -> tuple:
    password = password or random_string()
    user = create_user(password=password, nickname=nickname, email=email, telegram_nickname=telegram_nickname)
    sign_in_data = {'email': user.email, 'password': password}

    return user, client.post('/users/auth/sign_in/', data=sign_in_data)


def request_sign_up(client, first_name: str = None, last_name: str = None, nickname: str = None, email: str = None, password: str = None, confirm_password: str = None, telegram_nickname: str = None) -> tuple:
    user_password : str = password or random_string()

    sign_up_data : dict = {"first_name" : first_name or random_string(), 
        "last_name" : last_name or random_string(),
        "nickname" : nickname or random_string(), 
        "email" : email or random_string() + '@test.py', 
        "password" : user_password,
        "confirm_password" : user_password if confirm_password is None else confirm_password,
        "telegram_nickname" : telegram_nickname or random_string()}

    response = client.post('/users/auth/sign_up/', data=json.dumps(sign_up_data), headers=Header.json)
    user : User = User.query.filter_by(nickname=sign_up_data['nickname'], email=sign_up_data['email']).first()

    return user, response

def request_logout(client):
    return client.get('/users/auth/logout/')
