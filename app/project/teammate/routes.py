from flask.json import jsonify
from app.utils.request_type.JSON import JSON
from flask_classy import FlaskView, route
from sqlalchemy.orm.scoping import scoped_session
from ..decorators import project_required, project_authorship_required
from ..models import Project
from ...user.decorators import check_auth, user_exists_by_email, user_exists
from ...db import db
from ...decorators import request_validation_required
from app.user.models import User
from .schemas import post_teammate_schema, delete_teammate_schema, delete_teammate_role_schema


class Teammates(FlaskView):
    session: scoped_session = db.session

    @check_auth
    @user_exists_by_email(JSON)
    @project_required
    @request_validation_required(schema=post_teammate_schema, req_type=JSON)
    @project_authorship_required
    @route('/<int:project_id>/teammates/', methods=['POST'])
    def post(self, project: Project, validated_request : dict):

        user = User.query.filter_by(email=validated_request.get('email')).first()
        project.add_teammate(user.id, validated_request.get('role_ids'))

        return jsonify(), 201


    @check_auth
    @user_exists()
    @project_required
    @request_validation_required(schema=delete_teammate_schema)
    @project_authorship_required
    @route('/<int:project_id>/teammates/', methods=['DELETE'])
    def delete(self, project : Project, validated_request : dict):

        user = User.query.get(validated_request.get('user_id'))
        project.exclude_teammate(user.id)

        return jsonify(), 200


    @check_auth
    @user_exists()
    @project_required
    @request_validation_required(schema=delete_teammate_role_schema)
    @project_authorship_required
    @route('/<int:project_id>/delete_teammate_role/', methods=['DELETE'])
    def delete_teammate_role(self, project : Project, validated_request : dict):

        user = User.query.get(validated_request.get('user_id'))
        project.delete_teammate_role(user.id, validated_request.get('role_id'))

        return jsonify(), 200
