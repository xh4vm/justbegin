import json
from tests.functional.TestAuth import TestAuth
from tests.functional.base import BaseTestCase
from app.auth.responses import AuthResponses
from tests.functional.header import Header
from tests.functional.mocks.sign_up import *


class SignUpTestCase(BaseTestCase, TestAuth):

    def test_sign_up_bad_data_type(self):

        with self.app.test_client() as test_client:
            response = test_client.post('/auth/sign_up/', data="asd")
            assert response.status_code == 400
            assert json.loads(response.data) == AuthResponses.BAD_DATA_TYPE

    def test_sign_up_bad_confirm_password(self):

        with self.app.test_client() as test_client:
            response = test_client.post('/auth/sign_up/', data=json.dumps({
                'first_name': SignUpMock.first_name,
                'last_name': SignUpMock.last_name,
                'email': SignUpMock.email,
                'nickname': SignUpMock.nickname,
                'password': SignUpMock.password,
                'confirm_password': "asd",
                'telegram_nickname': SignUpMock.telegram_nickname
            }), headers=Header.json)
            assert response.status_code == 400
            assert json.loads(response.data) == AuthResponses.BAD_CONFIRM_PASSWORD

    def test_sign_up_success_jwt(self):

        with self.app.test_client() as test_client:
            response = test_client.post('/auth/sign_up/', data=json.dumps({
                'first_name': SignUpMock.first_name,
                'last_name': SignUpMock.last_name,
                'email': SignUpMock.email,
                'nickname': SignUpMock.nickname,
                'password': SignUpMock.password,
                'confirm_password': SignUpMock.confirm_password,
                'telegram_nickname': SignUpMock.telegram_nickname
            }), headers=Header.json)

            assert response.status_code == 303
            assert self.get_set_cookie_name(response) == 'access_token_cookie'
            assert self.get_jwt_identity(response) == 1
            assert self.get_jwt_claims(response) == {"email":SignUpMock.email,"nickname":SignUpMock.nickname,
                "avatar":SignUpMock.avatar,"first_name":SignUpMock.first_name,"last_name":SignUpMock.last_name}
            assert self.verify_exp_jwt(response) == True

    def test_sign_up_already_auth(self):

        with self.app.test_client() as test_client:
            test_client.post('/auth/sign_up/', data=json.dumps({
                'first_name': SignUpMock.first_name,
                'last_name': SignUpMock.last_name,
                'email': SignUpMock.email,
                'nickname': SignUpMock.nickname,
                'password': SignUpMock.password,
                'confirm_password': SignUpMock.confirm_password,
                'telegram_nickname': SignUpMock.telegram_nickname
            }), headers=Header.json)

            response = test_client.post('/auth/sign_up/', data=json.dumps({
                'first_name': SignUpMock.first_name,
                'last_name': SignUpMock.last_name,
                'email': SignUpMock.email,
                'nickname': SignUpMock.nickname,
                'password': SignUpMock.password,
                'confirm_password': SignUpMock.confirm_password,
                'telegram_nickname': SignUpMock.telegram_nickname
            }), headers=Header.json)

            assert response.status_code == 208
            assert json.loads(response.data) == AuthResponses.ALREADY_AUTH

    def test_sign_up_duplicate_email(self):

        with self.app.test_client() as test_client:
            SignUpMock.init()

            response = test_client.post('/auth/sign_up/', data=json.dumps({
                'first_name': SignUpMock.first_name,
                'last_name': SignUpMock.last_name,
                'email': SignUpMock.email,
                'nickname': SignUpMock.nickname,
                'password': SignUpMock.password,
                'confirm_password': SignUpMock.confirm_password,
                'telegram_nickname': SignUpMock.telegram_nickname
            }), headers=Header.json)

            assert response.status_code == 400
            assert json.loads(response.data) == AuthResponses.DUPLICATE_EMAIL