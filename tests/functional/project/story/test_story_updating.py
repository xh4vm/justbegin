from random import randint

from tests.functional.user.auth.utils import sign_in
from tests.functional.bases.base_without_create_project_author import BaseWithoutCreateProjectAuthorTestCase
from tests.functional.project.utils import create_project_story
from tests.utils import random_string


class ProjectStoryUpdate(BaseWithoutCreateProjectAuthorTestCase):

    def test_user_story_updated(self) -> None:
        with self.app.test_client() as client:
            user = sign_in(client)
            story = create_project_story(author_user_id=user.id)
            expected_story_title = random_string(64)
            expected_story_content = random_string(1024)

            request_data = {'title': expected_story_title, 'content': expected_story_content}
            response = client.put(f'/projects/stories/{story.id}', data=request_data)

            assert response.status_code == 200

            self.session.refresh(story)

            assert story.title == expected_story_title
            assert story.content == expected_story_content

    def test_user_can_update_just_story_title(self) -> None:
        with self.app.test_client() as client:
            user = sign_in(client)
            story = create_project_story(author_user_id=user.id)
            expected_story_title = random_string(64)
            expected_story_content = story.content

            request_data = {'title': expected_story_title}
            response = client.put(f'/projects/stories/{story.id}', data=request_data)

            assert response.status_code == 200

            self.session.refresh(story)

            assert story.title == expected_story_title
            assert story.content == expected_story_content

    def test_user_can_update_just_story_content(self) -> None:
        with self.app.test_client() as client:
            user = sign_in(client)
            story = create_project_story(author_user_id=user.id)
            expected_story_title = story.title
            expected_story_content = random_string(1024)

            request_data = {'content': expected_story_content}
            response = client.put(f'/projects/stories/{story.id}', data=request_data)

            assert response.status_code == 200

            self.session.refresh(story)

            assert story.title == expected_story_title
            assert story.content == expected_story_content

    def test_unauthorized_user_cannot_update_story(self) -> None:
        with self.app.test_client() as client:
            story = create_project_story()
            expected_story_content = story.content

            response = client.put(f'/projects/stories/{story.id}', data={'content': random_string(1024)})

            assert response.status_code == 401

            self.session.refresh(story)

            assert story.content == expected_story_content

    def test_user_cannot_update_story_without_title_and_content_simultaneously(self) -> None:
        with self.app.test_client() as client:
            user = sign_in(client)
            story = create_project_story(author_user_id=user.id)

            response = client.put(f'/projects/stories/{story.id}', data={})

            assert response.status_code == 400

    def test_user_cannot_update_someone_else_story(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)
            story = create_project_story()
            expected_story_content = story.content

            response = client.put(f'/projects/stories/{story.id}', data={'content': random_string(1024)})

            assert response.status_code == 403

            self.session.refresh(story)

            assert story.content == expected_story_content

    def test_user_cannot_update_nonexistent_story(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)
            nonexistent_story_id = randint(1, 100)

            response = client.put(f'/projects/stories/{nonexistent_story_id}', data={'content': random_string(1024)})

            assert response.status_code == 404
