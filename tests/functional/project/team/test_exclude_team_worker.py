import json
from app.auth.utils import get_auth_instance
from app.project.exceptions import ProjectExceptions
from tests.utils import random_string
from tests.functional.header import Header
from tests.functional.auth.utils import create_user, sign_in, request_logout
from tests.functional.bases.base import BaseTestCase
from tests.functional.project.utils import request_create_project
from tests.functional.auth.utils import sign_in
from app.project.team.models import TeamWorker, WorkerRole
from tests.functional.project.team.utils import add_team_worker_roles


class ProjectExcludeTeamWorkerTestCase(BaseTestCase):

    def test_exclude_team_worker_check_auth_fail(self):

        with self.app.test_client() as test_client:
            user = sign_in(test_client)
            project, response = request_create_project(test_client)
            request_logout(test_client)

            team_worker_data = {"user_id": user.id, "project_id": project.id}

            response = test_client.delete(f'/projects/{project.id}/exclude_team_worker/', data=team_worker_data)
            
            assert response.status_code == 401

    def test_exclude_team_worker_success(self):
        
        with self.app.test_client() as test_client:

            user = sign_in(test_client)
            project, response = request_create_project(test_client)

            team_worker_data = {"user_id": user.id, "project_id": project.id}

            response = test_client.delete(f'/projects/{project.id}/exclude_team_worker/', data=team_worker_data)

            assert response.status_code == 200
            assert len(TeamWorker.query.filter_by(user_id=user.id, project_id=project.id).all()) == 0

    def test_exclude_team_worker_multiple_success(self):
        
        with self.app.test_client() as test_client:

            user = sign_in(test_client)
            project, response = request_create_project(test_client)

            add_team_worker_roles(user.id, project.id, [WorkerRole.query.filter_by(name="Developer").first().id, WorkerRole.query.filter_by(name="Manager").first().id])

            team_worker_data = {"user_id": user.id, "project_id": project.id}

            response = test_client.delete(f'/projects/{project.id}/exclude_team_worker/', data=team_worker_data)

            assert response.status_code == 200
            assert len(TeamWorker.query.filter_by(user_id=user.id, project_id=project.id).all()) == 0

    def test_add_team_worker_users_not_exists(self):
        
        with self.app.test_client() as test_client:

            user = sign_in(test_client)
            project, response = request_create_project(test_client)

            team_worker_data = {"user_id": "asd", "project_id": project.id}

            response = test_client.delete(f'/projects/{project.id}/exclude_team_worker/', data=team_worker_data)

            assert response.status_code == 400
    
    def test_add_team_worker_wrong_author_project(self):
        
        with self.app.test_client() as test_client:

            sign_in(test_client)
            project, response = request_create_project(test_client)
            request_logout(test_client)

            user = sign_in(test_client)

            team_worker_data = {"user_id": user.id, "project_id": project.id}

            response = test_client.delete(f'/projects/{project.id}/exclude_team_worker/', data=team_worker_data)

            assert response.status_code == 400
            assert json.loads(response.data) == ProjectExceptions.IS_NOT_PROJECT_ADMIN

    def test_add_team_worker_project_required(self):
        
        with self.app.test_client() as test_client:

            user = sign_in(test_client)

            team_worker_data = {"user_id": user.id, "project_id": "1"}

            response = test_client.delete(f'/projects/1/exclude_team_worker/', data=team_worker_data)

            assert response.status_code == 404
