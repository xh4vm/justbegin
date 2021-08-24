import json
from app.project.serializers import serialize_project
from app.user.serializers import serialize_user
from tests.functional.user.auth.utils import request_logout, sign_in, create_user
from tests.functional.TestAuth import TestAuth
from flask import request
from tests.functional.bases.base import BaseTestCase
from tests.functional.header import Header
from tests.functional.project.utils import request_create_project


class UserGetTestCase(BaseTestCase):

    def test_user_get_check_auth_fail(self):

        with self.app.test_client() as test_client:
            user = sign_in(test_client)
            request_logout(test_client)

            response = test_client.get(f'/users/{user.nickname}/')
            assert response.status_code == 401
    
    def test_user_get_empty_projects_list_success(self):

        with self.app.test_client() as test_client:
            user = sign_in(test_client)
            request_logout(test_client)
            sign_in(test_client)

            response = test_client.get(f'/users/{user.nickname}/')

            assert response.status_code == 200

            data = json.loads(response.data)
            assert "user" in data.keys()
            assert data["user"] == serialize_user(user)

            assert "projects" in data.keys()
            assert data["projects"] == []

    def test_user_get_one_project_success(self):

        with self.app.test_client() as test_client:
            user = sign_in(test_client)
            project, response = request_create_project(test_client)
            request_logout(test_client)
            sign_in(test_client)

            response = test_client.get(f'/users/{user.nickname}/')
            
            assert response.status_code == 200
            
            data = json.loads(response.data)
            assert "user" in data.keys()
            assert data["user"] == serialize_user(user)

            assert "projects" in data.keys()
            assert data["projects"] == [serialize_project(project)]
