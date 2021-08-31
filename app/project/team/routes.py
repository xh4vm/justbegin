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
from .schemas import add_teammate_schema, delete_teammate_schema, delete_teammate_role_schema


class Teams(FlaskView):
    session: scoped_session = db.session

    @check_auth
    @user_exists_by_email(JSON)
    @project_required
    @request_validation_required(schema=add_teammate_schema, req_type=JSON)
    @verify_project_authorship
    @route('/<int:project_id>/add_teammate/', methods=['POST'])
    def add_teammate(self, project: Project, validated_request : dict):

        user = User.query.filter_by(email=validated_request.get('email')).first()
        project.add_teammate(user.id, validated_request.get('teammate_role_ids'))

        return jsonify(), 201


    @check_auth
    @user_exists()
    @project_required
    @request_validation_required(schema=delete_teammate_schema)
    @verify_project_authorship
    @route('/<int:project_id>/exclude_teammate/', methods=['DELETE'])
    def exclude_team_worker(self, project : Project, validated_request : dict):

        user = User.query.get(validated_request.get('user_id'))
        project.exclude_teammate(user.id)

        return jsonify(), 200


    @check_auth
    @user_exists()
    @project_required
    @request_validation_required(schema=delete_teammate_role_schema)
    @verify_project_authorship
    @route('/<int:project_id>/delete_teammate_role/', methods=['DELETE'])
    def delete_teammate_role(self, project : Project, validated_request : dict):

        user = User.query.get(validated_request.get('user_id'))
        project.delete_teammate_role(user.id, validated_request.get('teammate_role_id'))

        return jsonify(), 200
