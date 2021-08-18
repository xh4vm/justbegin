from flask.json import jsonify
from flask_classy import FlaskView, route
from sqlalchemy.orm.scoping import scoped_session

from .exceptions import UnexpectedProjectRelation
from .models import ProjectComment
from .schemas import post_comment_schema, put_comment_schema
from ..decorators import comment_authorship_required
from ..serializers import serialize_project_comments
from ... import db
from ...auth.decorators import user_required
from ...decorators import request_validation_required


class Comments(FlaskView):
    session: scoped_session = db.session

    @route('/<int:project_id>/comments', methods=['GET'])
    def index(self, project_id: int) -> tuple:
        comments = (self.session
                    .query(ProjectComment)
                    .filter(ProjectComment.project_id == project_id, ProjectComment.parent_comment_id == None)
                    .order_by(ProjectComment.created_at)
                    .all())

        return jsonify(serialize_project_comments(comments)), 200

    @user_required
    @request_validation_required(post_comment_schema)
    @route('/<int:project_id>/comments', methods=['POST'])
    def post(self, user_id: int, project_id: int, validated_request: dict) -> tuple:
        parent_comment_id = (validated_request.get('parent_comment_id')
                             if 'parent_comment_id' in validated_request
                             else None)

        try:
            comment = ProjectComment(project_id, user_id, validated_request.get('content'), parent_comment_id)
        except UnexpectedProjectRelation:
            return '', 400

        self.session.add(comment)
        self.session.commit()

        return jsonify({'id': comment.id}), 200

    @comment_authorship_required
    @request_validation_required(put_comment_schema)
    @route('/comments/<int:comment_id>', methods=['PUT'])
    def put(self, comment_id: int, validated_request: dict) -> tuple:
        comment = (self.session
                   .query(ProjectComment)
                   .filter(ProjectComment.id == comment_id)
                   .one())

        comment.content = validated_request.get('content')
        self.session.commit()

        return jsonify({'id': comment.id}), 200

    @comment_authorship_required
    @route('/comments/<int:comment_id>', methods=['DELETE'])
    def delete(self, comment_id: int) -> tuple:
        self.session.query(ProjectComment).filter(ProjectComment.id == comment_id).delete()
        self.session.commit()

        return jsonify({'id': comment_id}), 200


class CommentVotes(FlaskView):
    session: scoped_session = db.session

    @user_required
    @route('/<int:project_id>/comments/votes', methods=['GET'])
    def index(self, user_id: int, project_id: int) -> tuple:
        # TODO: Frontend needs to know which comments user has already voted for.
        pass

    @user_required
    @route('/comments/<int:comment_id>/votes/up', methods=['POST'])
    def up(self, user_id: int, comment_id: int):
        comment: ProjectComment = self.session.query(ProjectComment).filter(ProjectComment.id == comment_id).one()
        comment.upvote(user_id)

        return jsonify(), 200

    @user_required
    @route('/comments/<int:comment_id>/votes/down', methods=['POST'])
    def down(self, user_id: int, comment_id: int):
        comment: ProjectComment = self.session.query(ProjectComment).filter(ProjectComment.id == comment_id).one()
        comment.downvote(user_id)

        return jsonify(), 200

    @user_required
    @route('/comments/<int:comment_id>/votes/annul', methods=['POST'])
    def annul(self, user_id: int, comment_id: int):
        comment: ProjectComment = self.session.query(ProjectComment).filter(ProjectComment.id == comment_id).one()
        comment.annul_vote(user_id)

        return jsonify(), 200
