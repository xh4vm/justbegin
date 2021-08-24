from typing import List

## Circular imports into User Routes
# from app.project.comment.models import ProjectComment
# from app.project.models import Project
# from app.project.story.models import ProjectStory


def serialize_project(project) -> dict:
# def serialize_project(project: Project) -> dict:
    return {
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'website': project.website
    }


def serialize_project_comments(comments) -> list:
# def serialize_project_comments(comments: List[ProjectComment]) -> list:
    result = []

    for comment in comments:
        result.append({
            'id': comment.id,
            'author': {'id': comment.author.id, 'name': comment.author.nickname},
            'content': comment.content,
            'score': comment.score,
            'replies': serialize_project_comments(comment.replies),
            'created_at': comment.created_at,
            'updated_at': comment.updated_at,
        })

    return sorted(result, key=lambda c: c['score'], reverse=True)


def serialize_project_story(story) -> dict:
# def serialize_project_story(story: ProjectStory) -> dict:
    return {
        'id': story.id,
        'author': {
            'id': story.author.id,
            'name': story.author.nickname,
        },
        'title': story.title,
        'content': story.content,
        'created_at': story.created_at,
        'updated_at': story.updated_at,
    }
