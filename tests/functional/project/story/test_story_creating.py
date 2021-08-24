import json
from random import randint

from app.project.story.models import ProjectStory
from tests.functional.user.auth.utils import sign_in
from tests.functional.bases.base_without_create_project_author import BaseWithoutCreateProjectAuthorTestCase
from tests.functional.project.utils import create_project, random_string


class ProjectStoryCreating(BaseWithoutCreateProjectAuthorTestCase):

    def test_user_story_persisted(self) -> None:
        with self.app.test_client() as client:
            user = sign_in(client)
            project = create_project()
            # TODO: User team role.
            expected_story_title = random_string(64)
            expected_story_content = random_string(1024)

            request_data = {
                'title': expected_story_title,
                'content': expected_story_content,
            }

            response = client.post(f'/projects/{project.id}/stories', data=request_data)

            assert response.status_code == 200

            actual_story_id = json.loads(response.data)['id']
            actual_story = ProjectStory.query.get(actual_story_id)

            assert actual_story.author_user_id == user.id
            assert actual_story.project_id == project.id
            assert actual_story.title == expected_story_title
            assert actual_story.content == expected_story_content

    def test_user_must_have_story_author_role_to_publish_story(self) -> None:
        pass

    def test_unauthorized_user_cannot_create_story(self) -> None:
        with self.app.test_client() as client:
            project = create_project()

            request_data = {
                'title': random_string(64),
                'content': random_string(1024),
            }

            response = client.post(f'/projects/{project.id}/stories', data=request_data)

            assert response.status_code == 401

    def test_user_cannot_create_story_without_title(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)

            request_data = {'content': random_string(1024)}
            response = client.post(f'/projects/{create_project().id}/stories', data=request_data)

            assert response.status_code == 400

    def test_user_cannot_create_story_without_content(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)

            request_data = {'title': random_string(64)}
            response = client.post(f'/projects/{create_project().id}/stories', data=request_data)

            assert response.status_code == 400

    def test_user_cannot_publish_story_for_nonexistent_project(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)
            nonexistent_project_id = randint(1, 100)

            request_data = {
                'title': random_string(64),
                'content': random_string(1024),
            }

            response = client.post(f'/projects/{nonexistent_project_id}/stories', data=request_data)

            assert response.status_code == 404
