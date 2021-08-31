from tests.functional.user.auth.utils import sign_in
from tests.functional.bases.base import BaseTestCase
from tests.functional.project.utils import request_create_project
from tests.functional.user.auth.utils import sign_in
from app.project.team.models import Teammates, WorkerRole
from app import db 


class ProjectCreateAuthorTestCase(BaseTestCase):

    def test_create_author_project_success(self):

        with self.app.test_client() as test_client:
            user = sign_in(test_client)
            project, response = request_create_project(test_client)

            teammate = Teammates.query \
                .filter_by(user_id=user.id, project_id=project.id, teammate_role_id=WorkerRole.get_admin().id) \
                .first()
            
            assert response.status_code == 201
            assert teammate.user_id is not None

    