from functools import wraps

from flask import jsonify, request, abort

from .comment.models import ProjectComment
from .models import Project
from .responses import ProjectResponses
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
                    return jsonify(ProjectResponses.IS_NOT_PROJECT_ADMIN), 400
            else:
                return jsonify(ProjectResponses.BAD_PROJECT_ID_DATA), 400

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def comment_authorship_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = get_auth_instance()

        if not auth.already_auth():
            abort(401)

        user_id: int = get_auth_instance().get_current_user_data_from_token()[0]
        comment: ProjectComment = ProjectComment.query.get(kwargs.get('comment_id'))

        if user_id != comment.author_user_id:
            abort(403)

        return f(*args, **kwargs)

    return decorated_function
