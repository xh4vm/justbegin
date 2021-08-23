from app.auth.models import User
import json
from tests.functional.auth.utils import create_user, sign_in, sign_up_get_response
from tests.functional.TestAuth import TestAuth
from tests.functional.bases.base import BaseTestCase
from app.auth.exceptions import AuthExceptions


class SignUpTestCase(BaseTestCase, TestAuth):
    
    def test_sign_up_bad_confirm_password(self):

        with self.app.test_client() as test_client:
            user, response = sign_up_get_response(test_client, confirm_password='123')
            
            assert response.status_code == 400
            assert json.loads(response.data) == AuthExceptions.BAD_CONFIRM_PASSWORD

    def test_sign_up_success_jwt(self):

        with self.app.test_client() as test_client:
            user, response = sign_up_get_response(test_client)

            assert response.status_code == 303
            assert self.get_set_cookie_name(response) == 'access_token_cookie'
            assert self.get_jwt_identity(response) == 1
            assert self.get_jwt_claims(response) == {"email":user.email,"nickname":user.nickname,
                "avatar":user.avatar,"first_name":user.first_name,"last_name":user.last_name,
                "telegram_nickname": user.telegram_nickname}
            assert self.verify_exp_jwt(response) == True

    def test_sign_up_already_auth(self):

        with self.app.test_client() as test_client:
            sign_in(test_client)

            user, response = sign_up_get_response(test_client)

            assert response.status_code == 208
            assert json.loads(response.data) == AuthExceptions.ALREADY_AUTH

    def test_sign_up_duplicate_email(self):

        with self.app.test_client() as test_client:
            _user : User= create_user()
            user, response = sign_up_get_response(test_client, email=_user.email)

            assert response.status_code == 400
            assert json.loads(response.data) == AuthExceptions.DUPLICATE_EMAIL
