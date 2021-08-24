from typing import List
from app.user.models import User


def serialize_user(user : User) -> dict:
    return {
        'id': user.id,
        'nickname': user.nickname,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'telegram_nickname': user.telegram_nickname
    }
