from random import randint

from tests.functional.bases.base_without_create_project_author import BaseWithoutCreateProjectAuthorTestCase
from tests.functional.project.utils import create_project, create_project_story


class ProjectStoryList(BaseWithoutCreateProjectAuthorTestCase):

    def test_empty_story_list(self) -> None:
        with self.app.test_client() as client:
            response = client.get(f'/projects/{create_project().id}/stories')

            assert response.status_code == 200
            assert len(response.get_json()) == 0

    def test_not_empty_story_list(self) -> None:
        with self.app.test_client() as client:
            project = create_project()
            story_count = randint(1, 5)

            for i in range(story_count):
                create_project_story(project.id)

            response = client.get(f'/projects/{project.id}/stories')

            assert response.status_code == 200
            assert len(response.get_json()) == story_count

    def test_user_cannot_retrieve_nonexistent_project_stories(self) -> None:
        with self.app.test_client() as client:
            nonexistent_project_id = randint(1, 100)

            response = client.get(f'/projects/{nonexistent_project_id}/stories')

            assert response.status_code == 404
