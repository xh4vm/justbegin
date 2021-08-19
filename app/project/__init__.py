from flask import Blueprint

from .comment.routes import ProjectComments, ProjectCommentVotes
from .routes import Projects
from .story.routes import ProjectStories

bp = Blueprint('projects', __name__, url_prefix='/projects')

Projects.register(bp, route_base='/')
ProjectComments.register(bp, route_base='/')
ProjectCommentVotes.register(bp, route_base='/')
ProjectStories.register(bp, route_base='/')
