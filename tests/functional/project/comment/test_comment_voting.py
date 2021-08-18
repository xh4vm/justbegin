from tests.functional.auth.utils import sign_in
from tests.functional.base import BaseTestCase
from tests.functional.project.utils import create_project_comment, upvote_comment


class ProjectCommentUpvoting(BaseTestCase):

    def test_user_can_upvote_comment(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)
            comment = create_project_comment()
            initial_score = upvote_comment(comment)

            response = client.post(f'/projects/comments/{comment.id}/votes/up')

            assert response.status_code == 200
            assert comment.score == initial_score + 1

    def test_user_can_downvote_comment(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)
            comment = create_project_comment()
            initial_score = upvote_comment(comment)

            response = client.post(f'/projects/comments/{comment.id}/votes/down')

            assert response.status_code == 200
            assert comment.score == initial_score - 1

    def test_user_can_annul_their_comment_vote(self) -> None:
        with self.app.test_client() as client:
            user = sign_in(client)
            comment = create_project_comment()
            initial_score = upvote_comment(comment)
            comment.upvote(user.id)

            response = client.post(f'/projects/comments/{comment.id}/votes/annul')

            assert response.status_code == 200
            assert comment.score == initial_score

    def test_user_can_upvote_single_comment_just_once(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)
            comment = create_project_comment()
            initial_score = upvote_comment(comment)

            for _ in range(3):
                response = client.post(f'/projects/comments/{comment.id}/votes/up')
                assert response.status_code == 200

            assert comment.score == initial_score + 1

    def test_user_can_downvote_single_comment_just_once(self) -> None:
        with self.app.test_client() as client:
            sign_in(client)
            comment = create_project_comment()
            initial_score = upvote_comment(comment)

            for _ in range(3):
                response = client.post(f'/projects/comments/{comment.id}/votes/down')
                assert response.status_code == 200

            assert comment.score == initial_score - 1

    def test_unauthorized_user_cannot_upvote_comment(self) -> None:
        with self.app.test_client() as client:
            comment = create_project_comment()

            response = client.post(f'/projects/comments/{comment.id}/votes/up')
            assert response.status_code == 401

    def test_unauthorized_user_cannot_downvote_comment(self) -> None:
        with self.app.test_client() as client:
            comment = create_project_comment()

            response = client.post(f'/projects/comments/{comment.id}/votes/down')
            assert response.status_code == 401

    def test_unauthorized_user_cannot_annul_vote(self) -> None:
        with self.app.test_client() as client:
            comment = create_project_comment()

            response = client.post(f'/projects/comments/{comment.id}/votes/annul')
            assert response.status_code == 401
