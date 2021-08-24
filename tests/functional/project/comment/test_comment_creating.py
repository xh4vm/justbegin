import json
from random import randint

from app.project.comment.models import ProjectComment
from tests.functional.user.auth.utils import sign_in
from tests.functional.bases.base_without_create_project_author import BaseWithoutCreateProjectAuthorTestCase
from tests.functional.project.utils import create_project, random_string, create_project_comment


class ProjectCommentCreating(BaseWithoutCreateProjectAuthorTestCase):

    def test_user_comment_persisted(self) -> None:
        with self.app.test_client() as client:
            user = sign_in(client)
            project = create_project()
            expected_comment_content = random_string(256)

            request_data = {'content': expected_comment_content}
            response = client.post(f'/projects/{project.id}/comments', data=request_data)

            assert response.status_code == 200

            actual_comment_id = json.loads(response.data)['id']
            actual_comment = ProjectComment.query.get(actual_comment_id)

            assert actual_comment.author_user_id == user.id
            assert actual_comment.project_id == project.id
            assert actual_comment.content == expected_comment_content

    def test_user_comment_reply_persisted(self) -> None:
        with self.app.test_client() as client:
            user = sign_in(client)
            project = create_project()
            parent_comment = create_project_comment(project.id)
            expected_comment_content = random_string(256)

            request_data = {'content': expected_comment_content, 'parent_comment_id': parent_comment.id}
            response = client.post(f'/projects/{project.id}/comments', data=request_data)

            assert response.status_code == 200

            actual_comment_reply = parent_comment.replies[0]

            assert actual_comment_reply.author_user_id == user.id
            assert actual_comment_reply.project_id == project.id
            assert actual_comment_reply.content == expected_comment_content

    def test_unauthorized_user_cannot_create_comment(self) -> None:
        with self.app.test_client() as client:
            project = create_project()

            request_data = {'content': random_string(256)}
            response = client.post(f'/projects/{project.id}/comments', data=request_data)

            assert response.status_code == 401

    def test_user_cannot_create_comment_without_content(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)

            response = client.post(f'/projects/{create_project().id}/comments', data={})

            assert response.status_code == 400

    def test_reply_must_belong_to_same_project_as_parent_comment(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)
            project = create_project()
            parent_comment = create_project_comment(project.id)
            another_project = create_project()

            request_data = {'content': random_string(256), 'parent_comment_id': parent_comment.id}
            response = client.post(f'/projects/{another_project.id}/comments', data=request_data)

            assert response.status_code == 400

    def test_user_cannot_leave_comment_on_nonexistent_project(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)
            nonexistent_project_id = randint(1, 100)

            request_data = {'content': random_string(256)}

            response = client.post(f'/projects/{nonexistent_project_id}/comments', data=request_data)

            assert response.status_code == 404
