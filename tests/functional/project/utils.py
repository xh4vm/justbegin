from random import randint

from werkzeug.exceptions import abort

from app.db import db
from app.project.comment.models import ProjectComment
from app.project.follower.models import ProjectFollower
from app.project.models import Project
from app.project.story.models import ProjectStory
from tests.functional.auth.utils import create_user
from tests.utils import random_string


def request_create_project(client, title: str = None, description: str = None, website: str = None) -> Project:
    project_data = {
        'title': random_string(),
        'description': random_string(),
        'website': f"{random_string()}.com",
    }

    response = client.put('/projects/', data=project_data)

    if response.status_code >= 400:
        abort(response.status_code)

    return Project.query.filter_by(title=project_data['title'], description=project_data['description'], website=project_data['website']).first(), response

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


def create_project_story(project_id: int = None, author_user_id: int = None, title: str = None, content: str = None) -> ProjectStory:
    story = ProjectStory(
        project_id or create_project().id,
        author_user_id or create_user().id,
        title or random_string(63),
        content or random_string(1024),
    )

    db.session.add(story)
    db.session.commit()

    return story


def create_project_follower(user_id: int = None, project_id: int = None) -> ProjectFollower:
    follower = ProjectFollower(
        user_id or create_user().id,
        project_id or create_project().id,
    )

    db.session.add(follower)
    db.session.commit()

    return follower
