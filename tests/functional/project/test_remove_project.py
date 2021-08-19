import json
from tests.functional.auth.utils import sign_in

from app import db
from app.models import ProjectCreator
from app.project.models import Project
from app.project.exceptions import ProjectExceptions
from tests.functional.base import BaseTestCase
from tests.functional.project.utils import create_project


class ProjectRemoveTestCase(BaseTestCase):
    def test_remove_project_check_auth_fail(self):

        with self.app.test_client() as test_client:

            response = test_client.delete('/projects/remove/')
            assert response.status_code == 401

    def test_remove_project_check_auth_success(self):
        
        with self.app.test_client() as test_client:
            sign_in(test_client)
            project = create_project()

            #TODO
            db.session.add(ProjectCreator(user_id=1, project_id=project.id))
            db.session.commit()
        
            response = test_client.delete('/projects/remove/', data={"project_id": project.id})
            assert response.status_code == 200

    def test_remove_project_success(self):
        
        with self.app.test_client() as test_client:
            sign_in(test_client)
            project = create_project()

            db.session.add(ProjectCreator(user_id=1, project_id=project.id))
            db.session.commit()
        
            assert Project.query.get(project.id) is not None

            response = test_client.delete('/projects/remove/', data={"project_id": project.id})

            assert response.status_code == 200
            assert response.data.decode() == ""
            assert Project.query.get(project.id) is None

    def test_remove_project_bad_project_id_data(self):
        
        with self.app.test_client() as test_client:
            sign_in(test_client)
            project = create_project()

            db.session.add(ProjectCreator(user_id=1, project_id=1))
            db.session.commit()
        
            response = test_client.delete('/projects/remove/', data={"project_id": project.id + 1})
            assert response.status_code == 400
            assert json.loads(response.data) == ProjectExceptions.BAD_PROJECT_ID_DATA

    def test_remove_project_verify_authorship_fail(self):
        
        with self.app.test_client() as test_client:
            sign_in(test_client)
            project = create_project()
            
            db.session.add(ProjectCreator(user_id=1, project_id=1))
            db.session.commit()
            
            test_client.get('/auth/logout/')
            sign_in(test_client)

            response = test_client.delete('/projects/remove/', data={"project_id": project.id})
            assert response.status_code == 400
            assert json.loads(response.data) == ProjectExceptions.IS_NOT_PROJECT_ADMIN