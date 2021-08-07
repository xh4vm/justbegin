from app import responses
import json
from tests.functional.TestAuth import TestAuth
from tests.functional.base import BaseTestCase
from app.auth.responses import AuthResponses
from tests.functional.header import Header
from tests.functional.mocks.sign_up import *
from app.account.forms import SettingsForm, DeleteFeedback


class AccountTestCase(BaseTestCase, TestAuth):

    def test_index_page_auth(self):

        with self.app.test_client() as test_client:
            response = test_client.get('/account/', data=json.dumps({
                'email': SignUpMock.email,
                'password': SignUpMock.password
            }), headers = Header.json)

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

            settings = SettingsForm(nickname=SignUpMock.nickname, first_name=SignUpMock.first_name,
                last_name=SignUpMock.last_name, email=SignUpMock.email,
                telegram_nickname=SignUpMock.telegram_nickname, delete="Удалить аккаунт")

            response = test_client.post('/account/setting/', data=settings.data)
            #not_exists = User.query(User.id).filter_by(nickname = SignUpMock.nickname).first() is None
            not_exist = db.session.query(User.id).filter_by(nickname = SignUpMock.nickname).first() is None

            #assert not_exist
            assert response.status_code == 303

