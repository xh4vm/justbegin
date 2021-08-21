from app.auth.models import User
from flask import request, jsonify
from flask_classy import FlaskView, route
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.sql.functions import func

from app import db
from app.auth.decorators import user_required, check_auth
from app.auth.utils import get_auth_instance
from app.decorators import request_is_json, request_validation_required
from app.project.models import FavoriteProject
from app.project.decorators import verify_authorship
from .exceptions import ProjectExceptions
from .models import Project
from .serializers import serialize_project
from .schemas import post_like_schema, delete_project_schema, put_project_schema


class Projects(FlaskView):

    session: scoped_session = db.session

    def index(self):
        projects = (self.session
                    .query(Project)
                    .order_by(Project.created_at)
                    .all())

        return jsonify(list(map(serialize_project, projects))), 200

    @check_auth
    @request_validation_required(put_project_schema)
    @route("/", methods=["PUT"])
    def create(self, validated_request : dict):
        project = Project(validated_request.get('title'), validated_request.get('description'), validated_request.get('website'))
        self.session.add(project)
        self.session.commit()

        return jsonify({'id': project.id}), 200

    @user_required
    @route('/like/', methods=['POST'])
    @request_validation_required(post_like_schema)
    def like(self, user : User, validated_request: dict):
        project_id = validated_request.get('project_id')

        project = Project.query.get(project_id)

        if project is None:
            return jsonify(ProjectExceptions.BAD_PROJECT_ID_DATA), 400

        status = project.like(user.id)

        return jsonify({"status": "success", "count": project.get_count_likes(), "active": status}), 200

    @route('/status_favorites/', methods=['POST'])
    def status_favorites(self):
        projects = Project.query.with_entities(Project.id, func.count(FavoriteProject.project_id).label('count'))\
            .filter(Project.id == FavoriteProject.project_id)\
            .group_by(FavoriteProject.project_id).all()

        return jsonify({"status": "success", "projects": projects}), 200

    @check_auth
    @verify_authorship(request_key='project_id')
    @request_validation_required(delete_project_schema)
    @route('/remove/', methods=['DELETE'])
    def remove(self, validated_request: dict):
        project = Project.query.get(validated_request.get('project_id'))

        if project is None:
            return jsonify(ProjectExceptions.BAD_PROJECT_ID_DATA), 400

        self.session.delete(project)
        self.session.commit()

        return "", 200
