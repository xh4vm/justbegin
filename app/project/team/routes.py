from flask.json import jsonify
from app.utils.request_type.JSON import JSON
from flask_classy import FlaskView, route
from sqlalchemy.orm.scoping import scoped_session
from ..decorators import project_required, verify_project_authorship
from ..models import Project
from ...user.decorators import check_auth, user_exists_by_email, user_exists
from ...db import db
from ...decorators import request_validation_required
from app.user.models import User
from .schemas import put_team_worker_schema, delete_worker_role_schema, delete_team_worker_schema


class Teams(FlaskView):
    session: scoped_session = db.session

    @check_auth
    @user_exists_by_email(JSON)
    @project_required
    @request_validation_required(schema=put_team_worker_schema, req_type=JSON)
    @verify_project_authorship(req_type=JSON)
    @route('/<int:project_id>/add_team_worker/', methods=['POST'])
    def add_team_worker(self, project: Project, validated_request : dict):

        user = User.query.filter_by(email=validated_request.get('email')).first()
        project.add_worker(user.id, validated_request.get('worker_role_ids'))

        return jsonify(), 201


    @check_auth
    @user_exists()
    @project_required
    @request_validation_required(schema=delete_team_worker_schema)
    @verify_project_authorship()
    @route('/<int:project_id>/exclude_team_worker/', methods=['DELETE'])
    def exclude_team_worker(self, project : Project, validated_request : dict):

        user = User.query.get(validated_request.get('user_id'))
        project.exclude_worker(user.id)

        return jsonify(), 200


    @check_auth
    @user_exists()
    @project_required
    @request_validation_required(schema=delete_worker_role_schema)
    @verify_project_authorship()
    @route('/<int:project_id>/delete_worker_role/', methods=['DELETE'])
    def delete_worker_role(self, project : Project, validated_request : dict):

        user = User.query.get(validated_request.get('user_id'))
        project.delete_worker_role(user.id, validated_request.get('worker_role_id'))

        return jsonify(), 200
