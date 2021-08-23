import json
from random import randint

from tests.functional.bases.base_without_create_project_author import BaseWithoutCreateProjectAuthorTestCase
from tests.functional.project.comment.utils import comments_sorted_by_score
from tests.functional.project.utils import create_project, create_project_comment, upvote_comment


class ProjectCommentList(BaseWithoutCreateProjectAuthorTestCase):

    def test_empty_comment_list(self) -> None:
        with self.app.test_client() as client:
            project = create_project()

            response = client.get(f'/projects/{project.id}/comments')

            assert response.status_code == 200
            assert len(response.get_json()) == 0

    def test_not_empty_comment_list(self) -> None:
        with self.app.test_client() as client:
            project = create_project()
            comment_count = randint(1, 5)

            for i in range(comment_count):
                create_project_comment(project.id)

            response = client.get(f'/projects/{project.id}/comments')

            assert response.status_code == 200
            assert len(response.get_json()) == comment_count

    def test_comment_list_sorted_by_score(self) -> None:
        with self.app.test_client() as client:
            project = create_project()
            comment_count = randint(2, 5)

            for _ in range(comment_count):
                comment = create_project_comment(project.id)
                upvote_comment(comment)
                reply_count = randint(2, 5)

                for _ in range(reply_count):
                    reply = create_project_comment(parent_comment_id=comment.id, project_id=comment.project_id)
                    upvote_comment(reply)

            response = client.get(f'/projects/{project.id}/comments')
            comment_list = json.loads(response.data)

            assert response.status_code == 200
            assert comments_sorted_by_score(comment_list)

    def test_user_cannot_retrieve_nonexistent_project_comments(self) -> None:
        with self.app.test_client() as client:
            nonexistent_project_id = randint(1, 100)

            response = client.get(f'/projects/{nonexistent_project_id}/comments')

            assert response.status_code == 404
