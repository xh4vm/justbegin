from .teammate.models import Teammate
from app.utils.request_type.Form import Form
from app.utils.request_type import IRequestType
from functools import wraps
from flask import abort
from .comment.models import ProjectComment
from .models import Project
from .story.models import ProjectStory
from ..user.auth.utils import get_auth_instance


def project_authorship_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id, claims = get_auth_instance().get_current_user_data_from_token()

        if 'project' not in kwargs:
            abort(500)

        project = kwargs['project']

        if Teammate.query \
            .filter_by(user_id=user_id, project_id=project.id, role_id=Teammate.ADMIN) \
            .first() is None:
            abort(400)

        return f(*args, **kwargs)
    return decorated_function

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

def project_exists(req_type: IRequestType = Form):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            project_id = req_type().get().get('project_id')

            if Project.query.get(project_id) is None:
                abort(400)
            
            return f(*args, **kwargs)

        return decorated_function
    return decorator
