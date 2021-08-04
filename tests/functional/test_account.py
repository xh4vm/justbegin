from app import responses
import json
from tests.functional.TestAuth import TestAuth
from tests.functional.base import BaseTestCase
from app.auth.responses import AuthResponses
from tests.functional.header import Header
from tests.functional.mocks.sign_up import *


class AccountTestCase(BaseTestCase, TestAuth):

    def test_index_page_auth(self):

        with self.app.test_client() as test_client:
            response = test_client.get('/account/', data=json.dumps({
                'email': SignUpMock.email,
                'password': SignUpMock.password
            }), headers = Header.json)

            assert response.status_code == 302