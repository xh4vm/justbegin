from random import randint

from app.project.follower.models import ProjectFollower
from tests.functional.user.auth.utils import sign_in
from tests.functional.bases.base_without_create_project_author import BaseWithoutCreateProjectAuthorTestCase
from tests.functional.project.utils import create_project


class ProjectProjectFollowing(BaseWithoutCreateProjectAuthorTestCase):

    def test_project_follower_persisted(self) -> None:
        with self.app.test_client() as client:
            user = sign_in(client)
            project = create_project()

            response = client.post(f'/projects/{project.id}/followers')

            assert response.status_code == 200

            follower = (ProjectFollower.query
                        .filter(ProjectFollower.project_id == project.id,
                                ProjectFollower.user_id == user.id)
                        .one())

            assert follower is not None

    def test_unauthorized_user_cannot_follow_project(self) -> None:
        with self.app.test_client() as client:
            project = create_project()

            response = client.post(f'/projects/{project.id}/followers')

            assert response.status_code == 401

    def test_user_cannot_follow_nonexistent_project(self) -> None:
        with self.app.test_client() as client:
            user = sign_in(client)
            nonexistent_project_id = randint(1, 100)

            response = client.post(f'/projects/{nonexistent_project_id}/followers')

            assert response.status_code == 404

            follower = (ProjectFollower.query
                        .filter(ProjectFollower.project_id == nonexistent_project_id,
                                ProjectFollower.user_id == user.id)
                        .first())

            assert follower is None
