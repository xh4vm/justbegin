from flask import Blueprint

from .comment.routes import Comments, CommentUpvotes
from .routes import Projects

bp = Blueprint('projects', __name__, url_prefix='/projects')

Projects.register(bp, route_base='/')
Comments.register(bp, route_base='/')
CommentUpvotes.register(bp, route_base='/')
