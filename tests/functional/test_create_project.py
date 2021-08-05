import json
from tests.functional.base import BaseTestCase
from app.project.responses import ProjectResponses
from tests.functional.header import Header
from tests.functional.mocks.project import ProjectMock
from tests.functional.mocks.sign_up import SignUpMeMock
from app.models import Project, User


class ProjectCreateTestCase(BaseTestCase):

    def test_create_project_check_auth_fail(self):

        with self.app.test_client() as test_client:
            response = test_client.get('/project/create/')
            assert response.status_code == 303

    def test_create_project_check_auth_success(self):
        
        with self.app.test_client() as test_client:
            SignUpMeMock.init()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)
        
            response = test_client.get('/project/create/')
            assert response.status_code == 200
