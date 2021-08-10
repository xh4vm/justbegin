from app.project.responses import ProjectResponses
from functools import wraps
from flask import jsonify, redirect, request
from app.auth.utils import get_auth_instance
from app.models import ProjectCreator, Project


def verify_authorship(request_key: str):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            id, claims = get_auth_instance().get_current_user_data_from_token()
            project_id = request.json.get(request_key)

            if Project.query.get(project_id) is not None:
                if ProjectCreator.query.get((id, project_id)) is None:
                    return jsonify(ProjectResponses.IS_NOT_PROJECT_ADMIN), 400
            else:
                return jsonify(ProjectResponses.BAD_PROJECT_ID_DATA), 400

            return f(*args, **kwargs)
        return decorated_function
    return decorator
