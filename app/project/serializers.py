from app.project.comment.models import ProjectComment, ProjectCommentVote
from app.project.models import Project
from typing import List


def serialize_project(project: Project) -> dict:
    return {
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'website': project.website
    }


def serialize_project_comment(comment: ProjectComment) -> dict:
    # TODO: Sorting by score.

    result = {
        'id': comment.id,
        'author': {'id': comment.author.id, 'name': comment.author.nickname},
        'content': comment.content,
        'score': comment.score,
        'replies': [],
        'created_at': comment.created_at
    }

    for reply in comment.replies:
        result['replies'].append(serialize_project_comment(reply))

    return result
