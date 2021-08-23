import json
from tests.functional.auth.utils import create_user, sign_in
from app.auth.methods.JWTAuth import JWTAuth
from tests.functional.TestAuth import TestAuth
from tests.functional.bases.base import BaseTestCase
from app.auth.exceptions import AuthExceptions
from tests.functional.header import Header
from app.auth.models import User
from time import sleep


class ResetPasswordTestCase(BaseTestCase, TestAuth):

    def test_reset_already_auth(self):

        with self.app.test_client() as test_client:
            user = sign_in(test_client)

            response = test_client.post('/auth/reset/', data={'email': user.email})

            assert response.status_code == 208
            assert json.loads(response.data) == AuthExceptions.ALREADY_AUTH

    def test_reset_unknown_user(self):

        with self.app.test_client() as test_client:

            response = test_client.post('/auth/reset/', data={'email': 'xoklhyip@yandex.ru'})

            assert response.status_code == 400
            assert json.loads(response.data) == AuthExceptions.UNKNOWN_USER
    
    def test_reset_send_mail_success(self):

        with self.app.test_client() as test_client:
            user = create_user()

            response = test_client.post('/auth/reset/', data={'email': user.email})

            assert response.status_code == 201
            assert response.data.decode() == ""

    def test_reset_password_success_jwt(self):

        with self.app.test_client() as test_client:
            user = create_user()

            user = User.query.with_entities(User).filter_by(email=user.email).first()
            token = JWTAuth.get_token(user)
            new_password = 'new_password'

            response = test_client.put(f'/auth/reset/{token}/', data={'password': new_password})

            assert response.status_code == 200
            assert response.data.decode() == ""
            assert user.check_password(new_password) is True

    def test_reset_password_token_expired_jwt(self):

        with self.app.test_client() as test_client:
            user = create_user()

            token = JWTAuth.get_token(user=user, timedelta_min=0)
            old_password = user.password
            new_password = 'new_password'

            #Ждем протухания токена
            sleep(1)

            response = test_client.put(f'/auth/reset/{token}/', data={'password': new_password})

            assert response.status_code == 408
            assert json.loads(response.data) == AuthExceptions.RESET_TOKENT_EXPIRED
            assert user.password == old_password

    def test_reset_password_already_auth_jwt(self):

        with self.app.test_client() as test_client:
            user : User = sign_in(test_client)

            token : dict = JWTAuth.get_token(user=user)
            new_password : str = 'new_password'

            response = test_client.put(f'/auth/reset/{token}/', data={'password': new_password})

            assert response.status_code == 208
            assert json.loads(response.data) == AuthExceptions.ALREADY_AUTH
