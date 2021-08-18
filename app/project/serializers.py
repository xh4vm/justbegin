from typing import List

from app.project.comment.models import ProjectComment, ProjectCommentVote
from app.project.models import Project


def serialize_project(project: Project) -> dict:
    return {
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'website': project.website
    }


def serialize_project_comments(comments: List[ProjectComment]) -> list:
    result = []

    for comment in comments:
        result.append({
            'id': comment.id,
            'author': {'id': comment.author.id, 'name': comment.author.nickname},
            'content': comment.content,
            'score': comment.score,
            'replies': serialize_project_comments(comment.replies),
            'created_at': comment.created_at
        })

    return sorted(result, key=lambda c: c['score'], reverse=True)
