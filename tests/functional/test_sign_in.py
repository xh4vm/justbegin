import json
from tests.functional.TestAuth import TestAuth
from tests.functional.base import BaseTestCase
from app.auth.exceptions import AuthExceptions
from tests.functional.header import Header
from tests.functional.mocks.sign_up import *


class SignInTestCase(BaseTestCase, TestAuth):

    def test_sign_in_bad_data_type(self):

        with self.app.test_client() as test_client:
            response = test_client.post('/auth/sign_in/', data="asd")
            assert response.status_code == 400
            assert json.loads(response.data) == AuthExceptions.BAD_DATA_TYPE

    def test_sign_in_success_jwt(self):

        with self.app.test_client() as test_client:
            SignUpMock.init()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMock.email,
                'password': SignUpMock.password,
            }), headers=Header.json)

            assert response.status_code == 303
            assert self.get_set_cookie_name(response) == 'access_token_cookie'
            assert self.get_jwt_identity(response) == 1
            assert self.get_jwt_claims(response) == {"email":SignUpMock.email,"nickname":SignUpMock.nickname,
                "avatar":SignUpMock.avatar,"first_name":SignUpMock.first_name,"last_name":SignUpMock.last_name,"telegram_nickname":SignUpMock.telegram_nickname}
            assert self.verify_exp_jwt(response) == True

    def test_sign_in_bad_auth_data(self):

        with self.app.test_client() as test_client:
            SignUpMock.init()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMock.email,
                'password': 'asd',
            }), headers=Header.json)

            assert response.status_code == 400
            assert json.loads(response.data) == AuthExceptions.BAD_AUTH_DATA

    def test_sign_in_already_auth(self):

        with self.app.test_client() as test_client:
            SignUpMeMock.init()

            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)

            assert response.status_code == 208
            assert json.loads(response.data) == AuthExceptions.ALREADY_AUTH

    