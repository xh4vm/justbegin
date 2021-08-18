from app import responses
import json
from tests.functional.TestAuth import TestAuth
from tests.functional.base import BaseTestCase
from app.auth.responses import AuthResponses
from tests.functional.header import Header
from tests.functional.mocks.sign_up import *
from tests.functional.auth.utils import sign_in


class AccountTestCase(BaseTestCase, TestAuth):

    def test_failed_get_account_page(self):
        with self.app.test_client() as test_client:
            SignUpMock.init()

            response = test_client.get('/account/')
            assert response.status_code == 401

    def test_success_get_account_page(self):
        with self.app.test_client() as test_client:
            SignUpMock.init()

            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMock.email,
                'password': SignUpMock.password,
            }), headers=Header.json)

            response = test_client.get('/account/')

            assert response.status_code == 200
            assert json.loads(response.data) == {"avatar": None, "email": SignUpMock.email,
            "first_name": SignUpMock.first_name, "last_name": SignUpMock.last_name,
            "nickname": SignUpMock.nickname, "telegram_nickname": SignUpMock.telegram_nickname}

    def test_failed_get_settings_page(self):
        with self.app.test_client() as test_client:

            response = test_client.get('/account/settings/')
            assert response.status_code == 401
    
    def test_settings_post_form(self):
        with self.app.test_client() as test_client:
            SignUpMock.init()

            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMock.email,
                'password': SignUpMock.password,
            }), headers=Header.json)
            
            response = test_client.post('/account/settings/', data={
                'nickname': 'new_nickname',
                'first_name': 'new_first_name',
                'last_name': 'new_last_name',
                'email': 'new_email@mail.com',
                'telegram_nickname': 'new_telegram_nickname',
            })

            assert response.status_code == 303                       
            user = User.query.filter_by(nickname = 'new_nickname').first()
        
            assert user.nickname == 'new_nickname'
            assert user.first_name == 'new_first_name'
            assert user.last_name == 'new_last_name'
            assert user.email == 'new_email@mail.com'
            assert user.telegram_nickname == 'new_telegram_nickname'

    def test_settings_get_form(self):
        with self.app.test_client() as test_client:
            SignUpMock.init()
            
            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMock.email,
                'password': SignUpMock.password,
            }), headers=Header.json)

            response = test_client.get('/account/settings/')

            assert response.status_code == 200

            assert json.loads(response.data) == {"avatar": SignUpMock.avatar, "nickname": SignUpMock.nickname, 
            "first_name": SignUpMock.first_name, "last_name": SignUpMock.last_name,
            "email":SignUpMock.email, "telegram_nickname": SignUpMock.telegram_nickname}


    def test_settings_delete_post_form(self):
        with self.app.test_client() as test_client:
            SignUpMock.init()

            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMock.email,
                'password': SignUpMock.password,
            }), headers=Header.json)

            response = test_client.post('/account/delete/', data={
                'user_message': 'my dream is dead...',
            })

            not_exist = db.session.query(User.id).filter_by(nickname = SignUpMock.nickname).first() is None

            assert response.status_code == 303
            assert not_exist
            

    def test_settings_delete_get_form(self):
        with self.app.test_client() as test_client:
            SignUpMock.init()

            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMock.email,
                'password': SignUpMock.password,
            }), headers=Header.json)

            response = test_client.get('/account/delete/')

            assert response.status_code == 200
            assert json.loads(response.data) == {"nickname": SignUpMock.nickname}
