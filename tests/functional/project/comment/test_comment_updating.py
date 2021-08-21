from random import randint

from tests.functional.auth.utils import sign_in
from tests.functional.base import BaseTestCase
from tests.functional.project.utils import create_project_comment
from tests.utils import random_string


class ProjectCommentUpdate(BaseTestCase):

    def test_user_comment_updated(self) -> None:
        with self.app.test_client() as client:
            user = sign_in(client)
            comment = create_project_comment(author_user_id=user.id)
            expected_comment_content = random_string(256)

            response = client.put(f'/projects/comments/{comment.id}', data={'content': expected_comment_content})

            assert response.status_code == 200

            self.session.refresh(comment)

            assert comment.content == expected_comment_content

    def test_unauthorized_user_cannot_update_comment(self) -> None:
        with self.app.test_client() as client:
            comment = create_project_comment()
            expected_comment_content = comment.content

            response = client.put(f'/projects/comments/{comment.id}', data={'content': random_string(256)})

            assert response.status_code == 401

            self.session.refresh(comment)

            assert comment.content == expected_comment_content

    def test_user_cannot_update_comment_without_content(self) -> None:
        with self.app.test_client() as client:
            user = sign_in(client)
            comment = create_project_comment(author_user_id=user.id)

            response = client.put(f'/projects/comments/{comment.id}', data={})

            assert response.status_code == 400

    def test_user_cannot_update_someone_else_comment(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)
            comment = create_project_comment()
            expected_comment_content = comment.content

            response = client.put(f'/projects/comments/{comment.id}', data={'content': random_string(256)})

            assert response.status_code == 403

            self.session.refresh(comment)

            assert comment.content == expected_comment_content

    def test_user_cannot_update_nonexistent_comment(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)
            nonexistent_comment_id = randint(1, 100)

            response = client.put(f'/projects/comments/{nonexistent_comment_id}', data={'content': random_string(256)})

            assert response.status_code == 404
