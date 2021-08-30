from app.project.serializers import serialize_project
import json

from flask.globals import request
from tests.functional.user.auth.utils import request_logout, sign_in
from tests.functional.project.utils import create_project, request_like_project
from tests.functional.bases.base_without_create_project_author import BaseWithoutCreateProjectAuthorTestCase


class GetProjectListTestCase(BaseWithoutCreateProjectAuthorTestCase):

    def test_get_project_list_empty(self):

        with self.app.test_client() as test_client:

            response = test_client.get('/projects/')
            data = json.loads(response.data)

            assert response.status_code == 200
            assert len(data) == 0

    def test_get_project_list_one_project_zero_like(self):

        with self.app.test_client() as test_client:
            project = create_project()

            response = test_client.get('/projects/')
            data = json.loads(response.data)

            assert response.status_code == 200
            assert len(data) == 1
            assert data[0] == {**serialize_project(project), 'count_likes': 0}

    def test_get_project_list_one_project_one_like(self):

        with self.app.test_client() as test_client:
            sign_in(test_client)
            project = create_project()

            request_like_project(test_client, project.id)
    
            response = test_client.get('/projects/')
            data = json.loads(response.data)

            assert response.status_code == 200
            assert len(data) == 1
            assert data[0] == {**serialize_project(project), 'count_likes': 1}

    def test_get_project_list_one_project_one_like_one_dislike(self):

        with self.app.test_client() as test_client:
            sign_in(test_client)
            project = create_project()
        
            request_like_project(test_client, project.id)
            response = test_client.get('/projects/')
            
            request_like_project(test_client, project.id)
            response = test_client.get('/projects/')
            data = json.loads(response.data)

            assert response.status_code == 200
            assert len(data) == 1
            assert data[0] == {**serialize_project(project), 'count_likes': 0}

    def test_get_project_list_one_project_double_like(self):

        with self.app.test_client() as test_client:
            sign_in(test_client)
            project = create_project()
        
            request_like_project(test_client, project.id)
            request_logout(test_client)

            sign_in(test_client)
            request_like_project(test_client, project.id)

            response = test_client.get('/projects/')
            data = json.loads(response.data)

            assert response.status_code == 200
            assert len(data) == 1
            assert data[0] == {**serialize_project(project), 'count_likes': 2}
