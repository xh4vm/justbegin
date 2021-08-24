import json

from flask.globals import request
from tests.functional.user.auth.utils import request_logout, sign_in
from tests.functional.project.utils import create_project
from tests.functional.bases.base_without_create_project_author import BaseWithoutCreateProjectAuthorTestCase


class StatusFavoriteProjectsTestCase(BaseWithoutCreateProjectAuthorTestCase):

    def test_status_favorite_project_empty(self):

        with self.app.test_client() as test_client:

            response = test_client.post('/projects/status_favorites/')
            data = json.loads(response.data)

            assert response.status_code == 200
            assert data["status"] == "success"
            assert len(data["projects"]) == 0

    def test_status_favorite_project_one_project_zero_like(self):

        with self.app.test_client() as test_client:
            project = create_project()

            response = test_client.post('/projects/status_favorites/')
            data = json.loads(response.data)

            assert response.status_code == 200
            assert data["status"] == "success"
            assert len(data["projects"]) == 0

    def test_status_favorite_project_one_project_one_like(self):

        with self.app.test_client() as test_client:
            sign_in(test_client)
            project = create_project()

            test_client.post('/projects/like/', data={"project_id": project.id})
    
            response = test_client.post('/projects/status_favorites/')
            data = json.loads(response.data)

            assert response.status_code == 200
            assert data["status"] == "success"
            assert len(data["projects"]) == 1
            assert data["projects"][0][0] == 1
            assert data["projects"][0][1] == 1

    def test_status_favorite_project_one_project_one_like_one_dislike(self):

        with self.app.test_client() as test_client:
            sign_in(test_client)
            project = create_project()
        
            test_client.post('/projects/like/', data={"project_id": project.id})
            response = test_client.post('/projects/status_favorites/')
            
            test_client.post('/projects/like/', data={"project_id": project.id})
            response = test_client.post('/projects/status_favorites/')
            data = json.loads(response.data)

            assert response.status_code == 200
            assert data["status"] == "success"
            assert len(data["projects"]) == 0

    def test_status_favorite_project_one_project_double_like(self):

        with self.app.test_client() as test_client:
            sign_in(test_client)
            project = create_project()
        
            test_client.post('/projects/like/', data={"project_id": project.id})
            request_logout(test_client)

            sign_in(test_client)
            test_client.post('/projects/like/', data={"project_id": project.id})

            response = test_client.post('/projects/status_favorites/')
            data = json.loads(response.data)

            assert response.status_code == 200
            assert data["status"] == "success"
            assert len(data["projects"]) == 1
            assert data["projects"][0][0] == 1
            assert data["projects"][0][1] == 2
