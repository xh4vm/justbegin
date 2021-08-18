from flask import Blueprint

from .comment.routes import Comments, CommentVotes
from .routes import Projects

bp = Blueprint('projects', __name__, url_prefix='/projects')

Projects.register(bp, route_base='/')
Comments.register(bp, route_base='/')
CommentVotes.register(bp, route_base='/')
