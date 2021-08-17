import json

from app.models import FavoriteProject
from app.project.responses import ProjectResponses
from tests.functional.base import BaseTestCase
from tests.functional.header import Header
from tests.functional.mocks.sign_up import SignUpMeMock, SignUpMock
from tests.functional.project.utils import create_project


class ProjectFavoriteTestCase(BaseTestCase):

    def test_favorite_project_check_auth_fail(self):

        with self.app.test_client() as test_client:
            project = create_project()

            response = test_client.post('/projects/like/', data=json.dumps({"project_id": project.id}), headers=Header.json)

            assert response.status_code == 401

    '''
    def test_favorite_project_check_auth_success(self):
        
        with self.app.test_client() as test_client:
            SignUpMeMock.init()
            project = create_project()

            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)
        
            response = test_client.post('/projects/like/', data=json.dumps({"project_id": project.id}), headers=Header.json)
            assert response.status_code == 200

    def test_favorite_project_bad_project_id_data(self):
        
        with self.app.test_client() as test_client:
            SignUpMeMock.init()
            project = create_project()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)
        
            response = test_client.post('/projects/like/', data=json.dumps({"project_id": project.id00}), headers=Header.json)
            assert response.status_code == 400
            assert json.loads(response.data) == ProjectResponses.BAD_PROJECT_ID_DATA

    def test_favorite_project_bad_data_type(self):

        with self.app.test_client() as test_client:
            project = create_project()
            SignUpMeMock.init()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)

            response = test_client.post('/projects/like/', data="asd")

            assert response.status_code == 400
            assert json.loads(response.data) == ProjectResponses.BAD_DATA_TYPE

    def test_favorite_project_like_success(self):
        
        with self.app.test_client() as test_client:
            SignUpMeMock.init()
            project = create_project()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)
        
            assert FavoriteProject.query.get((1, 1)) is None

            response = test_client.post('/projects/like/', data=json.dumps({"project_id": project.id}), headers=Header.json)

            assert response.status_code == 200
            assert FavoriteProject.query.get((1, 1)) is not None
            assert json.loads(response.data) == {"status": "success", "count": 1, "active": True}
            #TODO: протестить изменения на странице

    def test_favorite_project_unlike_success(self):
        
        with self.app.test_client() as test_client:
            SignUpMeMock.init()
            project = create_project()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)
        
            assert FavoriteProject.query.get((1, 1)) is None

            response = test_client.post('/projects/like/', data=json.dumps({"project_id": project.id}), headers=Header.json)
            
            assert response.status_code == 200
            assert FavoriteProject.query.get((1, 1)) is not None
            assert json.loads(response.data) == {"status": "success", "count": 1, "active": True}
            #TODO: протестить изменения на странице

            response = test_client.post('/projects/like/', data=json.dumps({"project_id": project.id}), headers=Header.json)

            assert response.status_code == 200
            assert FavoriteProject.query.get((1, 1)) is None
            assert json.loads(response.data) == {"status": "success", "count": 0, "active": False}
            #TODO: протестить изменения на странице

    def test_favorite_project_multiple_user_like_like_unlike_success(self):
        
        with self.app.test_client() as test_client:
            SignUpMock.init()
            project = create_project()

            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMock.email,
                'password': SignUpMock.password,
            }), headers=Header.json)
        
            assert FavoriteProject.query.get((1, 1)) is None

            response = test_client.post('/projects/like/', data=json.dumps({"project_id": project.id}), headers=Header.json)
            
            assert response.status_code == 200
            assert FavoriteProject.query.get((1, 1)) is not None
            assert json.loads(response.data) == {"status": "success", "count": 1, "active": True}
            #TODO: протестить изменения на странице

            response = test_client.get('/auth/logout/')

            SignUpMeMock.init()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)

            response = test_client.post('/projects/like/', data=json.dumps({"project_id": project.id}), headers=Header.json)

            assert response.status_code == 200
            assert json.loads(response.data) == {"status": "success", "count": 2, "active": True}
            #TODO: протестить изменения на странице

            response = test_client.post('/projects/like/', data=json.dumps({"project_id": project.id}), headers=Header.json)

            assert response.status_code == 200
            assert FavoriteProject.query.get((2, 1)) is None
            assert json.loads(response.data) == {"status": "success", "count": 1, "active": False}
            #TODO: протестить изменения на странице
    '''