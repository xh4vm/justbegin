import json

from tests.functional.base import BaseTestCase
from tests.functional.project.utils import create_project_story


class ProjectStoryRetrieving(BaseTestCase):

    def test_user_can_retrieve_project_story(self) -> None:
        with self.app.test_client() as client:
            story = create_project_story()

            response = client.get(f'/projects/stories/{story.id}')
            response_data = json.loads(response.data)

            assert response.status_code == 200
            assert story.id == response_data['id']
            assert story.title == response_data['title']
            assert story.content == response_data['content']
            assert story.author.nickname == response_data['author']['name']
