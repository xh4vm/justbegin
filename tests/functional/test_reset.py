from app.auth.methods.JWTAuth import JWTAuth
import json
from tests.functional.TestAuth import TestAuth
from tests.functional.base import BaseTestCase
from app.auth.responses import AuthResponses
from tests.functional.header import Header
from tests.functional.mocks.sign_up import SignUpMeMock
from app.models import User
from time import sleep


class ResetPasswordTestCase(BaseTestCase, TestAuth):

    def test_reset_bad_data_type(self):

        with self.app.test_client() as test_client:
            response = test_client.post('/auth/reset/', data="asd")
            assert response.status_code == 400
            assert json.loads(response.data) == AuthResponses.BAD_DATA_TYPE

    def test_reset_already_auth(self):

        with self.app.test_client() as test_client:
            SignUpMeMock.init()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)

            response = test_client.post('/auth/reset/', data=json.dumps({
                'email': SignUpMeMock.email,
            }), headers=Header.json)

            assert response.status_code == 208
            assert json.loads(response.data) == AuthResponses.ALREADY_AUTH

    def test_reset_unknown_user(self):

        with self.app.test_client() as test_client:

            response = test_client.post('/auth/reset/', data=json.dumps({
                'email': 'xoklhyip@yandex.ru',
            }), headers=Header.json)

            assert response.status_code == 400
            assert json.loads(response.data) == AuthResponses.UNKNOWN_USER
    
    def test_reset_send_mail_success(self):

        with self.app.test_client() as test_client:
            SignUpMeMock.init()

            response = test_client.post('/auth/reset/', data=json.dumps({
                'email': SignUpMeMock.email,
            }), headers=Header.json)

            assert response.status_code == 201
            assert json.loads(response.data) == AuthResponses.TOKEN_CREATED

    def test_reset_password_success_jwt(self):

        with self.app.test_client() as test_client:
            SignUpMeMock.init()

            user = User.query.with_entities(User).filter_by(email=SignUpMeMock.email).first()
            token = JWTAuth.get_token(user)
            new_password = 'new_password'

            response = test_client.post(f'/auth/reset/{token}/', data=json.dumps({
                'password': new_password,
            }), headers=Header.json)

            assert response.status_code == 200
            assert json.loads(response.data) == AuthResponses.RESET_PASSWORD_SUCCESS
            assert user.check_password(new_password) is True

    def test_reset_password_token_expired_jwt(self):

        with self.app.test_client() as test_client:
            SignUpMeMock.init()

            user = User.query.with_entities(User).filter_by(email=SignUpMeMock.email).first()
            token = JWTAuth.get_token(user=user, timedelta_min=0)
            old_password = user.password
            new_password = 'new_password'

            #Ждем протухания токена
            sleep(1)

            response = test_client.post(f'/auth/reset/{token}/', data=json.dumps({
                'password': new_password,
            }), headers=Header.json)

            assert response.status_code == 408
            assert json.loads(response.data) == AuthResponses.RESET_TOKENT_EXPIRED
            assert user.password == old_password

    def test_reset_password_already_auth_jwt(self):

        with self.app.test_client() as test_client:
            SignUpMeMock.init()

            user = User.query.with_entities(User).filter_by(email=SignUpMeMock.email).first()
            token = JWTAuth.get_token(user=user)
            new_password = 'new_password'

            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)

            response = test_client.post(f'/auth/reset/{token}/', data=json.dumps({
                'password': new_password,
            }), headers=Header.json)

            assert response.status_code == 208
            assert json.loads(response.data) == AuthResponses.ALREADY_AUTH