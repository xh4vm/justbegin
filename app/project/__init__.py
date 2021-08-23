from flask import Blueprint

from .comment.routes import ProjectComments, ProjectCommentVotes
from .follower.routes import ProjectFollowers
from .routes import Projects
from .story.routes import ProjectStories
from .team.routes import Teams

bp = Blueprint('projects', __name__, url_prefix='/projects')

Projects.register(bp, route_base='/')
ProjectComments.register(bp, route_base='/')
ProjectCommentVotes.register(bp, route_base='/')
ProjectFollowers.register(bp, route_base='/')
ProjectStories.register(bp, route_base='/')
Teams.register(bp, route_base='/')
