from tests.functional.user.auth.utils import sign_in, request_logout
from tests.functional.bases.base import BaseTestCase
from tests.functional.project.utils import request_create_project
from tests.functional.user.auth.utils import sign_in
from app.project.team.models import Teammates, WorkerRole
from tests.functional.project.team.utils import add_team_worker_roles


class ProjectDeleteWorkerRoleTestCase(BaseTestCase):

    def test_delete_worker_role_check_auth_fail(self):

        with self.app.test_client() as test_client:
            user = sign_in(test_client)
            project, response = request_create_project(test_client)
            request_logout(test_client)

            team_worker_data = {"user_id": user.id, "project_id": project.id, "worker_role_id": WorkerRole.get_admin().id}

            response = test_client.delete(f'/projects/{project.id}/delete_worker_role/', data=team_worker_data)
            
            assert response.status_code == 401

    def test_delete_worker_role_success(self):
        
        with self.app.test_client() as test_client:

            user = sign_in(test_client)
            project, response = request_create_project(test_client)

            team_worker_data = {"user_id": user.id, "project_id": project.id, "worker_role_id": WorkerRole.get_admin().id}

            response = test_client.delete(f'/projects/{project.id}/delete_worker_role/', data=team_worker_data)

            assert response.status_code == 200
            assert len(Teammates.query.filter_by(user_id=user.id, project_id=project.id).all()) == 0

    def test_delete_worker_role_multiple_success(self):
        
        with self.app.test_client() as test_client:

            user = sign_in(test_client)
            project, response = request_create_project(test_client)

            add_team_worker_roles(user.id, project.id, [WorkerRole.query.filter_by(name="Developer").first().id, WorkerRole.query.filter_by(name="Manager").first().id])

            team_worker_data = {"user_id": user.id, "project_id": project.id, "worker_role_id": WorkerRole.get_admin().id}

            response = test_client.delete(f'/projects/{project.id}/delete_worker_role/', data=team_worker_data)

            assert response.status_code == 200
            assert len(Teammates.query.filter_by(user_id=user.id, project_id=project.id).all()) == 2
            assert Teammates.query.filter_by(user_id=user.id, project_id=project.id, worker_role_id=WorkerRole.get_admin().id).first() is None

    def test_delete_worker_role_users_not_exists(self):
        
        with self.app.test_client() as test_client:

            sign_in(test_client)
            project, response = request_create_project(test_client)

            team_worker_data = {"user_id": "asd", "project_id": project.id, "worker_role_id": WorkerRole.get_admin().id}

            response = test_client.delete(f'/projects/{project.id}/delete_worker_role/', data=team_worker_data)

            assert response.status_code == 400
    
    def test_delete_worker_role_wrong_author_project(self):
        
        with self.app.test_client() as test_client:

            sign_in(test_client)
            project, response = request_create_project(test_client)
            request_logout(test_client)

            user = sign_in(test_client)

            team_worker_data = {"user_id": user.id, "project_id": project.id, "worker_role_id": WorkerRole.get_admin().id}

            response = test_client.delete(f'/projects/{project.id}/delete_worker_role/', data=team_worker_data)

            assert response.status_code == 400

    def test_delete_worker_role_project_required(self):
        
        with self.app.test_client() as test_client:

            user = sign_in(test_client)

            team_worker_data = {"user_id": user.id, "project_id": "1", "worker_role_id": WorkerRole.get_admin().id}

            response = test_client.delete(f'/projects/1/delete_worker_role/', data=team_worker_data)

            assert response.status_code == 404
