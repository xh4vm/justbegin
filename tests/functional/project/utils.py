from random import randint

from app.db import db
from app.project.comment.models import ProjectComment
from app.project.models import Project
from tests.functional.auth.utils import create_user
from tests.utils import random_string


def create_project(title: str = None, description: str = None, website: str = None) -> Project:
    project = Project(
        title or random_string(),
        description or random_string(),
        website or random_string(),
    )

    db.session.add(project)
    db.session.commit()

    return project


def create_project_comment(project_id: int = None, author_user_id: int = None, content: str = None, parent_comment_id: int = None) -> ProjectComment:
    if author_user_id is None:
        author_user_id = create_user().id

    comment = ProjectComment(
        project_id or create_project().id,
        author_user_id or create_user().id,
        content or random_string(256),
        parent_comment_id
    )

    db.session.add(comment)
    db.session.commit()

    return comment


def upvote_comment(comment: ProjectComment, times: int = None) -> int:
    score = times or randint(0, 5)

    for i in range(score):
        comment.upvote(create_user().id)

    return score
