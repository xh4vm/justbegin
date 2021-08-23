import json
from random import choice

from tests.functional.auth.utils import sign_in
from tests.functional.bases.base_without_create_project_author import BaseWithoutCreateProjectAuthorTestCase
from tests.functional.project.utils import create_project, create_project_follower, create_project_story


class FollowedProjectsTimeline(BaseWithoutCreateProjectAuthorTestCase):

    def test_user_can_retrieve_stories_from_followed_projects(self) -> None:
        with self.app.test_client() as client:
            user = sign_in(client)

            followed_project_count = 3
            followed_project = []

            for _ in range(followed_project_count):
                project = create_project()
                create_project_follower(user.id, project.id)
                followed_project.append(project)

            expected_stories_count = 10
            expected_stories = {}

            for _ in range(expected_stories_count):
                story = create_project_story(choice(followed_project).id)
                expected_stories[story.id] = {'title': story.title, 'content': story.content}

            response = client.get(f'/projects/stories')

            assert response.status_code == 200

            actual_stories = json.loads(response.data)

            assert len(actual_stories) == expected_stories_count
            assert all(actual_stories[i]['created_at'] >= actual_stories[i + 1]['created_at']
                       for i in range(len(actual_stories) - 1))

            for actual_story in actual_stories:
                expected_story = expected_stories[actual_story['id']]

                assert actual_story['title'] == expected_story['title']
                assert actual_story['content'] == expected_story['content']
