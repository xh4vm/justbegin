import json

from tests.functional.base import BaseTestCase
from tests.functional.header import Header
from tests.functional.mocks.sign_up import SignUpMeMock, SignUpMock
from tests.functional.project.utils import create_project

'''
class StatusFavoriteProjectsTestCase(BaseTestCase):

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
            SignUpMeMock.init()
            project = create_project()

            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)
        
            test_client.post('/projects/like/', data=json.dumps({"project_id": project.id}), headers=Header.json)

            response = test_client.post('/projects/status_favorites/')
            data = json.loads(response.data)

            assert response.status_code == 200
            assert data["status"] == "success"
            assert len(data["projects"]) == 1
            assert data["projects"][0][0] == 1
            assert data["projects"][0][1] == 1

    def test_status_favorite_project_one_project_one_like_one_dislike(self):

        with self.app.test_client() as test_client:
            SignUpMeMock.init()
            project = create_project()

            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)
        
            test_client.post('/projects/like/', data=json.dumps({"project_id": project.id}), headers=Header.json)

            response = test_client.post('/projects/status_favorites/')
            data = json.loads(response.data)

            assert response.status_code == 200
            assert data["status"] == "success"
            assert len(data["projects"]) == 1
            assert data["projects"][0][0] == 1
            assert data["projects"][0][1] == 1

            test_client.post('/projects/like/', data=json.dumps({"project_id": project.id}), headers=Header.json)

            response = test_client.post('/projects/status_favorites/')
            data = json.loads(response.data)

            assert response.status_code == 200
            assert data["status"] == "success"
            assert len(data["projects"]) == 0

    def test_status_favorite_project_one_project_double_like(self):

        with self.app.test_client() as test_client:
            SignUpMeMock.init()
            project = create_project()

            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)
        
            test_client.post('/projects/like/', data=json.dumps({"project_id": project.id}), headers=Header.json)
            test_client.get('/auth/logout/')

            SignUpMock.init()

            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMock.email,
                'password': SignUpMock.password,
            }), headers=Header.json)
        
            test_client.post('/projects/like/', data=json.dumps({"project_id": project.id}), headers=Header.json)

            response = test_client.post('/projects/status_favorites/')
            data = json.loads(response.data)

            assert response.status_code == 200
            assert data["status"] == "success"
            assert len(data["projects"]) == 1
            assert data["projects"][0][0] == 1
            assert data["projects"][0][1] == 2
'''
