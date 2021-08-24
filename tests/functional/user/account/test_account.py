from sqlalchemy.orm.scoping import scoped_session
from app.user.models import User
import json
from app import db
from tests.functional.user.auth.utils import sign_in
from tests.functional.TestAuth import TestAuth
from tests.functional.bases.base_without_create_project_author import BaseTestCase
from app.user.auth.exceptions import AuthExceptions
from tests.functional.header import Header


class AccountTestCase(BaseTestCase, TestAuth):
    session : scoped_session = db.session

    def test_failed_get_account_page(self):
        with self.app.test_client() as test_client:
            response = test_client.get('/users/account/')
            assert response.status_code == 401

    def test_success_get_account_page(self):
        with self.app.test_client() as test_client:
            user = sign_in(test_client)

            response = test_client.get('/users/account/')

            assert response.status_code == 200
            assert json.loads(response.data) == {"avatar": None, "email": user.email,
            "first_name": user.first_name, "last_name": user.last_name,
            "nickname": user.nickname, "telegram_nickname": user.telegram_nickname}

    def test_failed_get_settings_page(self):
        with self.app.test_client() as test_client:

            response = test_client.get('/users/account/settings/')
            assert response.status_code == 401
    
    def test_settings_post_form(self):
        with self.app.test_client() as test_client:
            sign_in(test_client)
            
            response = test_client.post('/users/account/settings/', data=json.dumps({
                'nickname': 'new_nickname',
                'first_name': 'new_first_name',
                'last_name': 'new_last_name',
                'email': 'new_email@test.py',
                'telegram_nickname': 'new_telegram_nickname',
            }), headers=Header.json)

            assert response.status_code == 303                       
            user = User.query.filter_by(nickname = 'new_nickname').first()
        
            assert user.nickname == 'new_nickname'
            assert user.first_name == 'new_first_name'
            assert user.last_name == 'new_last_name'
            assert user.email == 'new_email@test.py'
            assert user.telegram_nickname == 'new_telegram_nickname'

    def test_settings_get_form(self):
        with self.app.test_client() as test_client:
            user = sign_in(test_client)

            response = test_client.get('/users/account/settings/')

            assert response.status_code == 200

            assert json.loads(response.data) == {"avatar": user.avatar, "nickname": user.nickname, 
            "first_name": user.first_name, "last_name": user.last_name,
            "email":user.email, "telegram_nickname": user.telegram_nickname}

    def test_settings_delete_post_form(self):
        with self.app.test_client() as test_client:
            user = sign_in(test_client)

            response = test_client.post('/users/account/delete/', data=json.dumps({
                'user_message': 'my dream is dead...',
            }), headers=Header.json)

            assert response.status_code == 303
            assert self.session.query(User.id).filter_by(nickname = user.nickname).first() is None

    def test_settings_delete_get_form(self):
        with self.app.test_client() as test_client:
            user = sign_in(test_client)

            response = test_client.get('/users/account/delete/')

            assert response.status_code == 200
            assert json.loads(response.data) == {"nickname": user.nickname}

