from app.project.comment.models import ProjectComment
from tests.functional.auth.utils import sign_in
from tests.functional.base import BaseTestCase
from tests.functional.project.utils import create_project_comment


class ProjectCommentDeleting(BaseTestCase):

    def test_user_comment_deleted(self) -> None:
        with self.app.test_client() as client:
            user = sign_in(client)
            comment = create_project_comment(author_user_id=user.id)
            response = client.delete(f'/projects/comments/{comment.id}')

            assert response.status_code == 200
            assert self.session.query(ProjectComment).get(comment.id) is None

    def test_unauthorized_user_cannot_delete_comment(self) -> None:
        with self.app.test_client() as client:
            comment = create_project_comment()

            response = client.delete(f'/projects/comments/{comment.id}')

            assert response.status_code == 401
            assert self.session.query(ProjectComment).get(comment.id) is not None

    def test_user_cannot_delete_someone_else_comment(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)
            comment = create_project_comment()

            response = client.delete(f'/projects/comments/{comment.id}')

            assert response.status_code == 403
            assert self.session.query(ProjectComment).get(comment.id) is not None