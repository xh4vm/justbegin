from tests.functional.auth.utils import sign_in, create_user
from werkzeug.wrappers.base_request import _assert_not_shallow
from tests.functional.TestAuth import TestAuth
from flask import request
from tests.functional.bases.base import BaseTestCase
from tests.functional.header import Header


class LogoutTestCase(BaseTestCase, TestAuth):

    def test_logout_no_login(self):

        with self.app.test_client() as test_client:
            response = test_client.get('/auth/logout/')
            assert response.status_code == 401
    
    def test_login_success_jwt(self):

        with self.app.test_client() as test_client:
            sign_in(test_client)

            response = test_client.get('/auth/logout/')

            assert response.status_code == 303
            assert self.get_set_cookie_name(response) == 'access_token_cookie'
            assert self.get_token(response) == ''

            response = test_client.get('/auth/logout/')

            assert response.status_code == 401

