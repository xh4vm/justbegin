import json
from app.auth import responses
from tests.functional.base import BaseTestCase
from app.auth.responses import AuthResponses
from tests.functional.header import Header
from tests.functional.mocks.sign_up import *


class SignInTestCase(BaseTestCase):

    def test_sign_in_bad_data_type(self):

        with self.app.test_client() as test_client:
            response = test_client.post('/auth/sign_in/', data="asd")
            assert response.status_code == 400
            assert json.loads(response.data) == AuthResponses.BAD_DATA_TYPE

    def test_sign_in_success(self):

        with self.app.test_client() as test_client:
            SignUpMock.init()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMock.email,
                'password': SignUpMock.password,
            }), headers=Header.json)

            assert response.status_code == 303

    def test_sign_in_bad_auth_data(self):

        with self.app.test_client() as test_client:
            SignUpMock.init()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMock.email,
                'password': 'asd',
            }), headers=Header.json)

            assert response.status_code == 400
            assert json.loads(response.data) == AuthResponses.BAD_AUTH_DATA

    