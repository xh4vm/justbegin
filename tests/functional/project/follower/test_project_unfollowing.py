from random import randint

from app.project.follower.models import ProjectFollower
from tests.functional.auth.utils import sign_in
from tests.functional.bases.base_without_create_project_author import BaseWithoutCreateProjectAuthorTestCase
from tests.functional.project.utils import create_project
from tests.functional.project.utils import create_project_follower


class ProjectProjectUnfollowing(BaseWithoutCreateProjectAuthorTestCase):

    def test_project_follower_deleted(self) -> None:
        with self.app.test_client() as client:
            user = sign_in(client)
            project = create_project()
            follower = create_project_follower(user.id, project.id)

            response = client.delete(f'/projects/{project.id}/followers')

            assert response.status_code == 200
            assert ProjectFollower.query.get(follower.id) is None

    def test_unauthorized_user_cannot_unfollow_project(self) -> None:
        with self.app.test_client() as client:
            project = create_project()

            response = client.delete(f'/projects/{project.id}/followers')

            assert response.status_code == 401

    def test_user_cannot_unfollow_nonexistent_project(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)
            nonexistent_project_id = randint(1, 100)

            response = client.delete(f'/projects/{nonexistent_project_id}/followers')

            assert response.status_code == 404
