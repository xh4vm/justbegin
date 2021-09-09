from tests.functional.user.auth.utils import request_logout, sign_in
from app.project.models import Project
from tests.functional.bases.base import BaseTestCase
from tests.functional.project.utils import create_project, request_create_project


class ProjectRemoveTestCase(BaseTestCase):
    def test_delete_project_check_auth_fail(self):

        with self.app.test_client() as test_client:
            sign_in(test_client)
            project = create_project()
            request_logout(test_client)

            response = test_client.delete(f'/projects/{project.id}/')
            assert response.status_code == 401

    def test_delete_project_check_auth_success(self):
        
        with self.app.test_client() as test_client:
            sign_in(test_client)
            project, response = request_create_project(test_client)
        
            response = test_client.delete(f'/projects/{project.id}/')
            assert response.status_code == 200

    def test_delete_project_success(self):
        
        with self.app.test_client() as test_client:
            sign_in(test_client)
            project, response = request_create_project(test_client)
        
            assert Project.query.get(project.id) is not None

            response = test_client.delete(f'/projects/{project.id}/')

            assert response.status_code == 200
            assert Project.query.get(project.id) is None

    def test_delete_project_bad_project_id_data(self):
        
        with self.app.test_client() as test_client:
            sign_in(test_client)
            project, response = request_create_project(test_client)

            response = test_client.delete(f'/projects/{project.id + 1}/')
            assert response.status_code == 404

    def test_delete_project_verify_authorship_fail(self):
        
        with self.app.test_client() as test_client:
            sign_in(test_client)
            project, response = request_create_project(test_client)

            request_logout(test_client)
            sign_in(test_client)

            response = test_client.delete(f'/projects/{project.id}/')
            assert response.status_code == 400
