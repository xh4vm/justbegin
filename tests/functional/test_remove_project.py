import json
from app import db
from tests.functional.base import BaseTestCase
from app.project.responses import ProjectResponses
from tests.functional.header import Header
from tests.functional.mocks.project import ProjectMock
from tests.functional.mocks.sign_up import SignUpMeMock, SignUpMock
from app.models import Project, User, ProjectCreator


class ProjectRemoveTestCase(BaseTestCase):
    def test_remove_project_check_auth_fail(self):

        with self.app.test_client() as test_client:

            response = test_client.post('/project/remove/', headers=Header.json)
            assert response.status_code == 303

    def test_remove_project_check_auth_success(self):
        
        with self.app.test_client() as test_client:
            SignUpMeMock.init()
            ProjectMock.init()
            db.session.add(ProjectCreator(user_id=1, project_id=1))
            db.session.commit()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)
        
            response = test_client.post('/project/remove/', data=json.dumps({"project_id": 1}), headers=Header.json)
            assert response.status_code == 200

    def test_remove_project_success(self):
        
        with self.app.test_client() as test_client:
            SignUpMeMock.init()
            ProjectMock.init()
            db.session.add(ProjectCreator(user_id=1, project_id=1))
            db.session.commit()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)
        
            assert Project.query.get(1) is not None

            response = test_client.post('/project/remove/', data=json.dumps({"project_id": 1}), headers=Header.json)

            right_response = ProjectResponses.SUCCESS_REMOVE.copy()
            right_response["message"] = right_response["message"].substitute(title=ProjectMock.title)

            assert response.status_code == 200
            assert json.loads(response.data) == right_response
            assert Project.query.get(1) is None

    def test_remove_project_bad_data_type(self):

        with self.app.test_client() as test_client:
            SignUpMeMock.init()
            ProjectMock.init()
            db.session.add(ProjectCreator(user_id=1, project_id=1))
            db.session.commit()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)

            response = test_client.post('/project/remove/', data="asd")

            assert response.status_code == 400
            assert json.loads(response.data) == ProjectResponses.BAD_DATA_TYPE

    def test_remove_project_bad_project_id_data(self):
        
        with self.app.test_client() as test_client:
            SignUpMeMock.init()
            ProjectMock.init()

            db.session.add(ProjectCreator(user_id=1, project_id=1))
            db.session.commit()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)
        
            response = test_client.post('/project/remove/', data=json.dumps({"project_id": 10000}), headers=Header.json)
            assert response.status_code == 400
            assert json.loads(response.data) == ProjectResponses.BAD_PROJECT_ID_DATA

    def test_remove_project_verify_authorship_fail(self):
        
        with self.app.test_client() as test_client:
            SignUpMock.init()
            ProjectMock.init()
            db.session.add(ProjectCreator(user_id=1, project_id=1))
            db.session.commit()
            
            SignUpMeMock.init()

            response = test_client.post('/auth/sign_in/', data=json.dumps({
                'email': SignUpMeMock.email,
                'password': SignUpMeMock.password,
            }), headers=Header.json)
        
            response = test_client.post('/project/remove/', data=json.dumps({"project_id": 1}), headers=Header.json)
            assert response.status_code == 400
            assert json.loads(response.data) == ProjectResponses.IS_NOT_PROJECT_ADMIN