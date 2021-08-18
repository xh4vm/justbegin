from tests.utils import random_string
from tests.functional.header import Header
from tests.functional.auth.utils import create_user, sign_in
from tests.functional.base import BaseTestCase


class ProjectCreateTestCase(BaseTestCase):

    def test_create_project_check_auth_fail(self):

        with self.app.test_client() as test_client:
            response = test_client.post('/projects/')
            assert response.status_code == 401

    def test_create_project_check_auth_success(self):
        
        with self.app.test_client() as test_client:

            sign_in(test_client)
            project_data = {
                'title': random_string(),
                'description': random_string(),
                'website': f"{random_string()}.com",
            }

            response = test_client.post('/projects/', data=project_data)

            assert response.status_code == 200
