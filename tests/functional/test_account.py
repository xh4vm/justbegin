from app import responses
import json
from tests.functional.TestAuth import TestAuth
from tests.functional.base import BaseTestCase
from app.auth.responses import AuthResponses
from tests.functional.header import Header
from tests.functional.mocks.sign_up import *
from app.account.forms import SettingsForm, DeleteFeedback


class AccountTestCase(BaseTestCase, TestAuth):

    def test_failed_get_account_page(self):

        with self.app.test_client() as test_client:
            SignUpMock.init()

            response = test_client.get('/account/')
            assert response.status_code == 303

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

    def test_delete_page_auth(self):

        with self.app.test_client() as test_client:
            SignUpMock.init()

            response = test_client.get('/account/delete/')
            assert response.status_code == 303

    def test_index_page_auth(self):

        with self.app.test_client() as test_client:
            SignUpMock.init()

            response = test_client.get('/account/')
            assert response.status_code == 303

    
    def test_setting_form(self):

        with self.app.test_client() as test_client:
            SignUpMock.init()

            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMock.email,
                'password': SignUpMock.password,
            }), headers=Header.json)

            settings = SettingsForm(nickname=SignUpMock.nickname, first_name=SignUpMock.first_name,
                last_name=SignUpMock.last_name, email=SignUpMock.email,
                telegram_nickname=SignUpMock.telegram_nickname, submit="Сохранить")    
            
            response = test_client.post('/account/setting/', data=settings.data)

            assert response.status_code == 303                       
            user = User.query.filter_by(nickname = SignUpMock.nickname).first()
        
            assert user.nickname == SignUpMock.nickname
            assert user.first_name == SignUpMock.first_name
            assert user.last_name == SignUpMock.last_name
            assert user.email == SignUpMock.email
            assert user.telegram_nickname == SignUpMock.telegram_nickname

    def test_setting_delete_form(self):

        with self.app.test_client() as test_client:
            SignUpMock.init()

            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMock.email,
                'password': SignUpMock.password,
            }), headers=Header.json)

            delete = DeleteFeedback(message='My dream is dead...', submit='Удалить аккаунт')

            response = test_client.post('/account/delete/', data=delete.data)
            not_exist = db.session.query(User.id).filter_by(nickname = SignUpMock.nickname).first() is None

            assert not_exist
            assert response.status_code == 303

