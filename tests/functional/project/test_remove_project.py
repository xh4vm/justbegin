import json

from app import db
from app.models import ProjectCreator
from app.project.models import Project
from app.project.responses import ProjectResponses
from tests.functional.base import BaseTestCase
from tests.functional.header import Header
from tests.functional.mocks.sign_up import SignUpMeMock, SignUpMock
from tests.functional.project.utils import create_project


class ProjectRemoveTestCase(BaseTestCase):
    def test_remove_project_check_auth_fail(self):

        with self.app.test_client() as test_client:

            response = test_client.post('/projects/remove/', headers=Header.json)
            assert response.status_code == 401

    def test_remove_project_check_auth_success(self):
        
        with self.app.test_client() as test_client:
            SignUpMeMock.init()
            project = create_project()
            db.session.add(ProjectCreator(user_id=1, project_id=project.id))
            db.session.commit()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)
        
            response = test_client.post('/projects/remove/', data=json.dumps({"project_id": project.id}), headers=Header.json)
            assert response.status_code == 200

    def test_remove_project_success(self):
        
        with self.app.test_client() as test_client:
            SignUpMeMock.init()
            project = create_project()
            db.session.add(ProjectCreator(user_id=1, project_id=project.id))
            db.session.commit()

            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)
        
            assert Project.query.get(project.id) is not None

            response = test_client.post('/projects/remove/', data=json.dumps({"project_id": project.id}), headers=Header.json)

            right_response = ProjectResponses.SUCCESS_REMOVE.copy()
            right_response["message"] = right_response["message"].substitute(title=project.title)

            assert response.status_code == 200
            assert json.loads(response.data) == right_response
            assert Project.query.get(project.id) is None

    def test_remove_project_bad_data_type(self):

        with self.app.test_client() as test_client:
            SignUpMeMock.init()
            db.session.add(ProjectCreator(user_id=1, project_id=1))
            db.session.commit()

            test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)

            response = test_client.post('/projects/remove/', data="asd")

            assert response.status_code == 400
            assert json.loads(response.data) == ProjectResponses.BAD_DATA_TYPE

    def test_remove_project_bad_project_id_data(self):
        
        with self.app.test_client() as test_client:
            SignUpMeMock.init()
            project = create_project()

            db.session.add(ProjectCreator(user_id=1, project_id=1))
            db.session.commit()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)
        
            response = test_client.post('/projects/remove/', data=json.dumps({"project_id": project.id + 1}), headers=Header.json)
            assert response.status_code == 400
            assert json.loads(response.data) == ProjectResponses.BAD_PROJECT_ID_DATA

    def test_remove_project_verify_authorship_fail(self):
        
        with self.app.test_client() as test_client:
            SignUpMock.init()
            project = create_project()
            db.session.add(ProjectCreator(user_id=1, project_id=1))
            db.session.commit()
            
            SignUpMeMock.init()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)
        
            response = test_client.post('/projects/remove/', data=json.dumps({"project_id": project.id}), headers=Header.json)
            assert response.status_code == 400
            assert json.loads(response.data) == ProjectResponses.IS_NOT_PROJECT_ADMIN