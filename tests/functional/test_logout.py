import json

from werkzeug.wrappers.base_request import _assert_not_shallow
from tests.functional.TestAuth import TestAuth
from flask import request
from tests.functional.base import BaseTestCase
from tests.functional.header import Header
from tests.functional.mocks.sign_up import SignUpMeMock


class LogoutTestCase(BaseTestCase, TestAuth):

    def test_logout_no_login(self):

        with self.app.test_client() as test_client:
            response = test_client.get('/auth/logout/')
            assert response.status_code == 401
    
    def test_login_success_jwt(self):

        with self.app.test_client() as test_client:
            SignUpMeMock.init()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)

            response = test_client.get('/auth/logout/')

            assert response.status_code == 303
            assert self.get_set_cookie_name(response) == 'access_token_cookie'
            assert self.get_token(response) == ''

            response = test_client.get('/auth/logout/')

            assert response.status_code == 401





