from .decorators import check_auth, user_exists, user_required
from flask import request, jsonify
from flask_classy import FlaskView, route
from sqlalchemy.orm.scoping import scoped_session
from .serializers import serialize_user
from ..project.serializers import serialize_project
from app import db
from .exceptions import UserExceptions
from .models import User


class Users(FlaskView):
    session : scoped_session = db.session

    @check_auth
    @route('/<nickname>/', methods=['GET'])
    def get_user(self, nickname : str):
        user = User.query.filter_by(nickname=nickname).first()

        return jsonify({"user": serialize_user(user), 
            "projects": list(map(serialize_project, user.projects_development))}), 200
