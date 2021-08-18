import json

from app.db import db
from app.models import User
from tests.functional.header import Header
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
    password = random_string()
    user = create_user(password=password)
    sign_in_data = json.dumps({'email': user.email, 'password': password})

    client.post('/auth/sign_in/', data=sign_in_data, headers=Header.json)

    return user
