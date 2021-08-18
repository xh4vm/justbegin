from tests.functional.auth.utils import sign_in
from tests.functional.base import BaseTestCase
from tests.functional.project.utils import create_project_comment, upvote_comment


class ProjectCommentUpvoting(BaseTestCase):

    def test_comment_upvote_persisted(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)
            comment = create_project_comment()
            initial_score = upvote_comment(comment)

            response = client.post(f'/projects/comments/{comment.id}/upvotes')

            assert response.status_code == 200
            assert comment.score == initial_score + 1

    def test_user_cannot_upvote_single_comment_repeatedly(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)
            comment = create_project_comment()
            initial_score = upvote_comment(comment)

            for _ in range(3):
                response = client.post(f'/projects/comments/{comment.id}/upvotes')
                assert response.status_code == 200

            assert comment.score == initial_score + 1

    def test_user_can_delete_their_comment_upvote(self) -> None:
        with self.app.test_client() as client:
            user = sign_in(client)
            comment = create_project_comment()
            initial_score = upvote_comment(comment)
            comment.upvote(user.id)

            response = client.delete(f'/projects/comments/{comment.id}/upvotes')

            assert response.status_code == 200
            assert comment.score == initial_score

    def test_unauthorized_user_cannot_upvote_comment(self) -> None:
        with self.app.test_client() as client:
            comment = create_project_comment()

            response = client.post(f'/projects/comments/{comment.id}/upvotes')
            assert response.status_code == 401

    def test_unauthorized_user_cannot_delete_upvote(self) -> None:
        with self.app.test_client() as client:
            comment = create_project_comment()

            response = client.delete(f'/projects/comments/{comment.id}/upvotes')
            assert response.status_code == 401
