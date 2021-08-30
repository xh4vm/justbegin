from app.user.models import User
from flask import jsonify
from flask_classy import FlaskView, route
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.sql.functions import func

from app import db
from ..user.decorators import user_required, check_auth
from app.decorators import request_validation_required
from app.project.models import FavoriteProject
from app.project.decorators import project_required, verify_project_authorship
from .models import Project
from .serializers import serialize_project_with_count_likes
from .schemas import create_project_schema
from sqlalchemy.sql.expression import null
from itertools import chain


class Projects(FlaskView):

    session: scoped_session = db.session

    def index(self):
        projects_with_likes = (Project
                    .query
                    .with_entities(*Project.__table__.columns, func.count(FavoriteProject.project_id).label('count_likes'))
                    .filter(Project.id == FavoriteProject.project_id)
                    .group_by(FavoriteProject.project_id))

        projects = (Project
                    .query
                    .with_entities(*Project.__table__.columns, null().label('count_likes'))
                    .filter(
                        ~Project.id.in_(
                            chain(*self.session.query(FavoriteProject.project_id).all())
                        )
                    )
                    .union(projects_with_likes)
                    .order_by(Project.created_at)
                    .all())

        return jsonify(list(map(serialize_project_with_count_likes, projects))), 200

    @check_auth
    @request_validation_required(create_project_schema)
    @route("/", methods=["POST"])
    def create(self, validated_request : dict):
        project = Project(validated_request.get('title'), validated_request.get('description'), validated_request.get('website'))
        self.session.add(project)
        self.session.commit()

        return jsonify({'id': project.id}), 201

    @user_required
    @project_required
    @route('/<int:project_id>/like/', methods=['POST'])
    def like(self, user : User, project: Project):

        status = project.like(user.id)
        return jsonify({"count": project.get_count_likes(), "active": status}), 200

    @check_auth
    @project_required
    @verify_project_authorship
    @route('/<int:project_id>/delete/', methods=['DELETE'])
    def delete(self, project: Project):

        self.session.delete(project)
        self.session.commit()

        return jsonify(), 200
