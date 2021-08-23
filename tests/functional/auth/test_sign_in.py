import json
from app.auth.models import User
from tests.functional.auth.utils import create_user, sign_in, sign_in_get_response
from tests.functional.TestAuth import TestAuth
from tests.functional.bases.base import BaseTestCase
from app.auth.exceptions import AuthExceptions
from tests.functional.header import Header


class SignInTestCase(BaseTestCase, TestAuth):

    def test_sign_in_success_jwt(self):

        with self.app.test_client() as test_client:
            user, response = sign_in_get_response(test_client)

            assert response.status_code == 303
            assert self.get_set_cookie_name(response) == 'access_token_cookie'
            assert self.get_jwt_identity(response) == 1
            assert self.get_jwt_claims(response) == {"email":user.email,"nickname":user.nickname,
                "avatar":user.avatar,"first_name":user.first_name,"last_name":user.last_name,
                "telegram_nickname":user.telegram_nickname}
            assert self.verify_exp_jwt(response) == True

    def test_sign_in_bad_auth_data(self):

        with self.app.test_client() as test_client:
            user : User = create_user()
            response = test_client.post('/auth/sign_in/', data={'email':user.email, 'password': '123'})

            assert response.status_code == 400
            assert json.loads(response.data) == AuthExceptions.BAD_AUTH_DATA

    def test_sign_in_already_auth(self):

        with self.app.test_client() as test_client:
            user = sign_in(test_client)

            response = test_client.post('/auth/sign_in/', data={'email': user.email,'password': user.password})

            assert response.status_code == 208
            assert json.loads(response.data) == AuthExceptions.ALREADY_AUTH
