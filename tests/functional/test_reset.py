import json
from tests.functional.TestAuth import TestAuth

from tests.functional.base import BaseTestCase
from app.auth.responses import AuthResponses
from tests.functional.Header import Header
from tests.functional.mocks.sign_up import SignUpMeMock


class ResetPasswordTestCase(BaseTestCase, TestAuth):

    def test_reset_bad_data_type(self):

        with self.app.test_client() as test_client:
            response = test_client.post('/auth/reset/', data="asd")
            assert response.status_code == 400
            assert json.loads(response.data) == AuthResponses.BAD_DATA_TYPE

    def test_reset_unknown_user(self):

        with self.app.test_client() as test_client:

            response = test_client.post('/auth/reset/', data=json.dumps({
                'email': 'xoklhyip@yandex.ru',
            }), headers=Header.json)

            assert response.status_code == 400
            assert json.loads(response.data) == AuthResponses.UNKNOWN_USER
    
    def test_reset_success(self):

        with self.app.test_client() as test_client:
            SignUpMeMock.init()

            response = test_client.post('/auth/reset/', data=json.dumps({
                'email': SignUpMeMock.email,
            }), headers=Header.json)

            assert response.status_code == 201
            assert json.loads(response.data) == AuthResponses.TOKEN_CREATED

