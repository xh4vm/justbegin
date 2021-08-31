from app.project.team.models import Teammates
import json
from tests.functional.header import Header
from tests.functional.user.auth.utils import create_user, sign_in, request_logout
from tests.functional.bases.base import BaseTestCase
from tests.functional.project.utils import request_create_project
from tests.functional.header import Header
from tests.functional.user.auth.utils import sign_in
from app import db 


class ProjectAddTeamWorkerTestCase(BaseTestCase):

    def test_add_teammate_check_auth_fail(self):

        with self.app.test_client() as test_client:
            user = sign_in(test_client)
            project, response = request_create_project(test_client)
            request_logout(test_client)

            teammate_data = {"email": user.email, "project_id": project.id, "teammate_role_ids": [Teammates.get_role_id("Editor"), Teammates.get_role_id("Reviewer")]}

            response = test_client.post(f'/projects/{project.id}/add_teammate/', data=json.dumps(teammate_data), headers=Header.json)
            
            assert response.status_code == 401

    def test_add_teammate_success(self):
        
        with self.app.test_client() as test_client:

            user = sign_in(test_client)
            project, response = request_create_project(test_client)

            teammate_data = {"email": user.email, "project_id": project.id, "teammate_role_ids": [Teammates.get_role_id("Editor"), Teammates.get_role_id("Reviewer")]}

            response = test_client.post(f'/projects/{project.id}/add_teammate/', data=json.dumps(teammate_data), headers=Header.json)

            assert response.status_code == 201

    def test_add_teammate_users_not_exists(self):
        
        with self.app.test_client() as test_client:

            user = sign_in(test_client)
            project, response = request_create_project(test_client)

            teammate_data = {"email": "asd", "project_id": project.id, "teammate_role_ids": [Teammates.get_role_id("Editor"), Teammates.get_role_id("Reviewer")]}

            response = test_client.post(f'/projects/{project.id}/add_teammate/', data=json.dumps(teammate_data), headers=Header.json)

            assert response.status_code == 400
    
    def test_add_teammate_wrong_author_project(self):
        
        with self.app.test_client() as test_client:

            sign_in(test_client)
            project, response = request_create_project(test_client)
            request_logout(test_client)

            user = sign_in(test_client)

            teammate_data = {"email": user.email, "project_id": project.id, "teammate_role_ids": [Teammates.get_role_id("Editor"), Teammates.get_role_id("Reviewer")]}

            response = test_client.post(f'/projects/{project.id}/add_teammate/', data=json.dumps(teammate_data), headers=Header.json)

            assert response.status_code == 400

    def test_add_teammate_project_required(self):
        
        with self.app.test_client() as test_client:

            user = sign_in(test_client)

            teammate_data = {"email": user.email, "project_id": "1", "teammate_role_ids": [Teammates.get_role_id("Editor"), Teammates.get_role_id("Reviewer")]}

            response = test_client.post(f'/projects/1/add_teammate/', data=json.dumps(teammate_data), headers=Header.json)

            assert response.status_code == 404
