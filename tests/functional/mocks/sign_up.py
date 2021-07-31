from app import db
from app.models import User


class SignUpMock:
    first_name = "FirstName"
    last_name = "LastName"
    nickname = "Nickname"
    email = "Email@gmail.com"
    avatar = None
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

class SignUpMeMock:
    first_name = "Kirill"
    last_name = "Epifanov"
    nickname = "xh4vm"
    email = "xoklhyip@yandex.ru"
    avatar = None
    password = "Password"
    confirm_password = "Password"
    telegram_nickname = "xh4vm"

    @staticmethod
    def init():
        user = User(first_name=SignUpMeMock.first_name, last_name=SignUpMeMock.last_name,
                    nickname=SignUpMeMock.nickname, email=SignUpMeMock.email, 
                    password=SignUpMeMock.password, telegram_nickname=SignUpMeMock.telegram_nickname)
        db.session.add(user)
        db.session.commit()