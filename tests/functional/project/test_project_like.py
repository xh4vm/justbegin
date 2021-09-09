import json
from tests.functional.user.auth.utils import request_logout, sign_in

from app.project.models import ProjectLike
from tests.functional.bases.base_without_create_project_author import BaseWithoutCreateProjectAuthorTestCase
from tests.functional.project.utils import create_project, request_create_project, request_like_project


class ProjectLikeTestCase(BaseWithoutCreateProjectAuthorTestCase):

    def test_favorite_project_check_auth_fail(self):

        with self.app.test_client() as test_client:
            project = create_project()

            response = request_like_project(test_client, project.id)

            assert response.status_code == 401

    
    def test_favorite_project_check_auth_success(self):
        
        with self.app.test_client() as test_client:
            sign_in(test_client)
            project = create_project()

            response = request_like_project(test_client, project.id)
            assert response.status_code == 200

    def test_favorite_project_bad_project_id_data(self):
        
        with self.app.test_client() as test_client:
            sign_in(test_client)
            
            project, response = request_create_project(test_client)

            response = request_like_project(test_client, project.id + 1)
            assert response.status_code == 404

    def test_favorite_project_like_success(self):
        
        with self.app.test_client() as test_client:
            user = sign_in(test_client)
            project = create_project()

            assert ProjectLike.query.filter_by(user_id=user.id, project_id=project.id).first() is None

            response = request_like_project(test_client, project.id)

            assert response.status_code == 200
            assert ProjectLike.query.filter_by(user_id=user.id, project_id=project.id).first() is not None
            assert json.loads(response.data) == {"count": 1, "active": True}

    def test_favorite_project_unlike_success(self):
        
        with self.app.test_client() as test_client:
            user = sign_in(test_client)
            project = create_project()

            assert ProjectLike.query.filter_by(user_id=user.id, project_id=project.id).first() is None

            response = request_like_project(test_client, project.id)
            
            assert response.status_code == 200
            assert ProjectLike.query.filter_by(user_id=user.id, project_id=project.id).first() is not None
            assert json.loads(response.data) == {"count": 1, "active": True}

            response = request_like_project(test_client, project.id)

            assert response.status_code == 200
            assert ProjectLike.query.filter_by(user_id=user.id, project_id=project.id).first() is None
            assert json.loads(response.data) == {"count": 0, "active": False}

    def test_favorite_project_multiple_user_like_like_unlike_success(self):
        
        with self.app.test_client() as test_client:
            user = sign_in(test_client)
            project = create_project()
        
            assert ProjectLike.query.filter_by(user_id=user.id, project_id=project.id).first() is None

            response = request_like_project(test_client, project.id)
            
            assert response.status_code == 200
            assert ProjectLike.query.filter_by(user_id=user.id, project_id=project.id).first() is not None
            assert json.loads(response.data) == {"count": 1, "active": True}

            response = request_logout(test_client)

            other_user = sign_in(test_client)

            response = request_like_project(test_client, project.id)

            assert response.status_code == 200
            assert json.loads(response.data) == {"count": 2, "active": True}

            response = request_like_project(test_client, project.id)

            assert response.status_code == 200
            assert ProjectLike.query.filter_by(user_id=other_user.id, project_id=project.id).first() is None
            assert json.loads(response.data) == {"count": 1, "active": False}
