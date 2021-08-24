from random import randint

from app.project.story.models import ProjectStory
from tests.functional.user.auth.utils import sign_in
from tests.functional.bases.base_without_create_project_author import BaseWithoutCreateProjectAuthorTestCase
from tests.functional.project.utils import create_project_story


class ProjectStoryDeleting(BaseWithoutCreateProjectAuthorTestCase):

    def test_user_story_deleted(self) -> None:
        with self.app.test_client() as client:
            user = sign_in(client)
            story = create_project_story(author_user_id=user.id)
            response = client.delete(f'/projects/stories/{story.id}')

            assert response.status_code == 200
            assert self.session.query(ProjectStory).get(story.id) is None

    def test_unauthorized_user_cannot_delete_story(self) -> None:
        with self.app.test_client() as client:
            story = create_project_story()

            response = client.delete(f'/projects/stories/{story.id}')

            assert response.status_code == 401
            assert self.session.query(ProjectStory).get(story.id) is not None

    def test_user_must_be_author_to_delete_story(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)
            story = create_project_story()

            response = client.delete(f'/projects/stories/{story.id}')

            assert response.status_code == 403
            assert self.session.query(ProjectStory).get(story.id) is not None

    def test_user_cannot_delete_nonexistent_story(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)
            nonexistent_story_id = randint(1, 100)

            response = client.delete(f'/projects/stories/{nonexistent_story_id}')

            assert response.status_code == 404
