from functools import wraps

from flask import jsonify, request, abort

from .comment.models import ProjectComment
from .models import Project
from .exceptions import ProjectExceptions
from .story.models import ProjectStory
from ..auth.utils import get_auth_instance
from ..models import ProjectCreator


def verify_authorship(request_key: str):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            id, claims = get_auth_instance().get_current_user_data_from_token()
            project_id = request.form.get(request_key)

            if Project.query.get(project_id) is not None:
                if ProjectCreator.query.get((id, project_id)) is None:
                    return jsonify(ProjectExceptions.IS_NOT_PROJECT_ADMIN), 400
            else:
                return jsonify(ProjectExceptions.BAD_PROJECT_ID_DATA), 400

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def project_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'project_id' not in kwargs:
            abort(400)

        project = Project.query.get(kwargs['project_id'])

        if project is None:
            abort(404)

        kwargs['project'] = project
        del kwargs['project_id']

        return f(*args, **kwargs)

    return decorated_function


def project_story_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'story_id' not in kwargs:
            abort(400)

        story = ProjectStory.query.get(kwargs['story_id'])

        if story is None:
            abort(404)

        kwargs['story'] = story
        del kwargs['story_id']

        return f(*args, **kwargs)

    return decorated_function


def project_story_authorship_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = get_auth_instance()

        if not auth.already_auth():
            abort(401)

        if 'story_id' not in kwargs:
            abort(400)

        user_id: int = get_auth_instance().get_current_user_data_from_token()[0]
        story: ProjectStory = ProjectStory.query.get(kwargs.get('story_id'))

        if story is None:
            abort(404)

        if user_id != story.author_user_id:
            abort(403)

        kwargs['story'] = story
        del kwargs['story_id']

        return f(*args, **kwargs)

    return decorated_function


def project_comment_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'comment_id' not in kwargs:
            abort(400)

        comment = ProjectComment.query.get(kwargs['comment_id'])

        if comment is None:
            abort(404)

        kwargs['comment'] = comment
        del kwargs['comment_id']

        return f(*args, **kwargs)

    return decorated_function


def project_comment_authorship_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = get_auth_instance()

        if not auth.already_auth():
            abort(401)

        if 'comment_id' not in kwargs:
            abort(400)

        user_id: int = get_auth_instance().get_current_user_data_from_token()[0]
        comment: ProjectComment = ProjectComment.query.get(kwargs.get('comment_id'))

        if comment is None:
            abort(404)

        if user_id != comment.author_user_id:
            abort(403)

        kwargs['comment'] = comment
        del kwargs['comment_id']

        return f(*args, **kwargs)

    return decorated_function
