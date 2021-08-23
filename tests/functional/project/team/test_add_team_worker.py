import json
from app.auth.utils import get_auth_instance
from app.project.exceptions import ProjectExceptions
from tests.utils import random_string
from tests.functional.header import Header
from tests.functional.auth.utils import create_user, sign_in, request_logout
from tests.functional.bases.base import BaseTestCase
from tests.functional.project.utils import request_create_project
from tests.functional.header import Header
from tests.functional.auth.utils import sign_in
from app.project.team.models import WorkerRole
from app import db 


class ProjectAddTeamWorkerTestCase(BaseTestCase):

    def test_add_team_worker_check_auth_fail(self):

        with self.app.test_client() as test_client:
            user = sign_in(test_client)
            project, response = request_create_project(test_client)
            request_logout(test_client)

            team_worker_data = {"email": user.email, "project_id": project.id, "worker_role_ids": [WorkerRole.query.filter_by(name="Developer").first().id, WorkerRole.query.filter_by(name="Manager").first().id]}

            response = test_client.put(f'/projects/{project.id}/add_team_worker/', data=json.dumps(team_worker_data), headers=Header.json)
            
            assert response.status_code == 401

    def test_add_team_worker_success(self):
        
        with self.app.test_client() as test_client:

            user = sign_in(test_client)
            project, response = request_create_project(test_client)

            team_worker_data = {"email": user.email, "project_id": project.id, "worker_role_ids": [WorkerRole.query.filter_by(name="Developer").first().id, WorkerRole.query.filter_by(name="Manager").first().id]}

            response = test_client.put(f'/projects/{project.id}/add_team_worker/', data=json.dumps(team_worker_data), headers=Header.json)

            assert response.status_code == 201

    def test_add_team_worker_users_not_exists(self):
        
        with self.app.test_client() as test_client:

            user = sign_in(test_client)
            project, response = request_create_project(test_client)

            team_worker_data = {"email": "asd", "project_id": project.id, "worker_role_ids": [WorkerRole.query.filter_by(name="Developer").first().id, WorkerRole.query.filter_by(name="Manager").first().id]}

            response = test_client.put(f'/projects/{project.id}/add_team_worker/', data=json.dumps(team_worker_data), headers=Header.json)

            assert response.status_code == 400
    
    def test_add_team_worker_wrong_author_project(self):
        
        with self.app.test_client() as test_client:

            sign_in(test_client)
            project, response = request_create_project(test_client)
            request_logout(test_client)

            user = sign_in(test_client)

            team_worker_data = {"email": user.email, "project_id": project.id, "worker_role_ids": [WorkerRole.query.filter_by(name="Developer").first().id, WorkerRole.query.filter_by(name="Manager").first().id]}

            response = test_client.put(f'/projects/{project.id}/add_team_worker/', data=json.dumps(team_worker_data), headers=Header.json)

            assert response.status_code == 400
            assert json.loads(response.data) == ProjectExceptions.IS_NOT_PROJECT_ADMIN

    def test_add_team_worker_project_required(self):
        
        with self.app.test_client() as test_client:

            user = sign_in(test_client)

            team_worker_data = {"email": user.email, "project_id": "1", "worker_role_ids": [WorkerRole.query.filter_by(name="Developer").first().id, WorkerRole.query.filter_by(name="Manager").first().id]}

            response = test_client.put(f'/projects/1/add_team_worker/', data=json.dumps(team_worker_data), headers=Header.json)

            assert response.status_code == 404
