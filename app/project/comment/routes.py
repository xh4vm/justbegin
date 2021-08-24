from flask.json import jsonify
from flask_classy import FlaskView, route
from sqlalchemy.orm.scoping import scoped_session

from .exceptions import UnexpectedProjectRelation, OwnCommentVoting
from .models import ProjectComment
from .schemas import post_comment_schema, put_comment_schema
from ..decorators import project_required, project_comment_required, project_comment_authorship_required
from ..models import Project
from ..serializers import serialize_project_comments
from ... import db
from ...user.decorators import user_required
from ...decorators import request_validation_required
from app.user.models import User


class ProjectComments(FlaskView):
    session: scoped_session = db.session

    @project_required
    @route('/<int:project_id>/comments', methods=['GET'])
    def index(self, project: Project) -> tuple:
        return jsonify(serialize_project_comments(project.parentless_comments)), 200

    @project_required
    @user_required
    @request_validation_required(post_comment_schema)
    @route('/<int:project_id>/comments', methods=['POST'])
    def post(self, user: User, project: Project, validated_request: dict) -> tuple:
        try:
            comment = project.leave_comment(user,
                                            validated_request.get('content'),
                                            validated_request.get('parent_comment_id'))
        except UnexpectedProjectRelation:
            return '', 400

        return jsonify({'id': comment.id}), 200

    @project_comment_authorship_required
    @request_validation_required(put_comment_schema)
    @route('/comments/<int:comment_id>', methods=['PUT'])
    def put(self, comment: ProjectComment, validated_request: dict) -> tuple:
        comment.content = validated_request.get('content')
        self.session.commit()

        return jsonify({'id': comment.id}), 200

    @project_comment_authorship_required
    @route('/comments/<int:comment_id>', methods=['DELETE'])
    def delete(self, comment: ProjectComment) -> tuple:
        self.session.delete(comment)
        self.session.commit()

        return jsonify({'id': comment.id}), 200


class ProjectCommentVotes(FlaskView):
    session: scoped_session = db.session

    @user_required
    @route('/<int:project_id>/comments/votes', methods=['GET'])
    def index(self, user: User, project_id: int) -> tuple:
        # TODO: Frontend needs to know which comments user has already voted for.
        pass

    @user_required
    @project_comment_required
    @route('/comments/<int:comment_id>/votes/up', methods=['POST'])
    def up(self, user: User, comment: ProjectComment):
        try:
            comment.upvote(user.id)
        except OwnCommentVoting:
            return jsonify(), 400

        return jsonify(), 200

    @user_required
    @project_comment_required
    @route('/comments/<int:comment_id>/votes/down', methods=['POST'])
    def down(self, user: User, comment: ProjectComment):
        try:
            comment.downvote(user.id)
        except OwnCommentVoting:
            return jsonify(), 400

        return jsonify(), 200

    @user_required
    @project_comment_required
    @route('/comments/<int:comment_id>/votes/annul', methods=['POST'])
    def annul(self, user: User, comment: ProjectComment):
        try:
            comment.annul_vote(user.id)
        except OwnCommentVoting:
            return jsonify(), 400

        return jsonify(), 200
