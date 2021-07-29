from app import db
from app.models import User


class SignUpMock:
    first_name = "FirstName"
    last_name = "LastName"
    nickname = "Nickname"
    email = "Email"
    password = "Password"
    confirm_password = "Password"
    telegram_nickname = "TelegramNickname"

    @staticmethod
    def init():
        user = User(first_name=SignUpMock.first_name, last_name=SignUpMock.last_name,
                    nickname=SignUpMock.nickname, email=SignUpMock.email, 
                    password=SignUpMock.password, telegram_nickname=SignUpMock.telegram_nickname)
        db.session.add(user)
        db.session.commit()