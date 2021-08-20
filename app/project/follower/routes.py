from flask import jsonify
from flask_classy import FlaskView, route

from ..decorators import project_required
from ..models import Project
from ...auth.decorators import user_required
from ...models import User


class ProjectFollowers(FlaskView):

    @user_required
    @project_required
    @route('/<int:project_id>/followers', methods=['POST'])
    def post(self, user: User, project: Project) -> tuple:
        project.follow(user)

        return jsonify(), 200

    @user_required
    @project_required
    @route('/<int:project_id>/followers', methods=['DELETE'])
    def delete(self, user: User, project: Project) -> tuple:
        project.unfollow(user)

        return jsonify(), 200
