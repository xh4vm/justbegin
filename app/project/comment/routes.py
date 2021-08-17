from flask.json import jsonify
from flask_classy import FlaskView, route
from sqlalchemy import and_
from sqlalchemy.orm.scoping import scoped_session

from .models import ProjectComment
from .schemas import post_comment_schema, put_comment_schema
from ..decorators import request_validation_required, comment_authorship_required
from ..serializers import serialize_project_comment
from ... import db
from ...auth.decorators import user_required


# TODO:
# - tests;
class Comments(FlaskView):
    session: scoped_session = db.session

    @route('/<int:project_id>/comments', methods=['GET'])
    def index(self, project_id: int) -> tuple:
        comments = (self.session
                    .query(ProjectComment)
                    .filter(and_(ProjectComment.project_id == project_id, ProjectComment.parent_comment_id == None))
                    .order_by(ProjectComment.created_at)
                    .all())

        return jsonify(list(map(serialize_project_comment, comments))), 200

    @user_required
    @request_validation_required(post_comment_schema)
    @route('/<int:project_id>/comments', methods=['POST'])
    def post(self, user_id: int, project_id: int, validated_request: dict) -> tuple:
        comment: ProjectComment = ProjectComment(
            project_id,
            user_id,
            validated_request.get('content'),
            validated_request.get('parent_comment_id') if 'parent_comment_id' in validated_request else None
        )

        self.session.add(comment)
        self.session.commit()

        return jsonify({'id': comment.id}), 200

    @comment_authorship_required
    @request_validation_required(put_comment_schema)
    @route('/comments/<int:comment_id>', methods=['PUT'])
    def put(self, comment_id: int, validated_request: dict) -> tuple:
        comment: ProjectComment = (self.session
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


class CommentUpvotes(FlaskView):
    session: scoped_session = db.session

    @user_required
    @route('/<int:project_id>/comments/upvotes')
    def index(self, user_id: int, project_id: int) -> tuple:
        pass

    @user_required
    @route('/comments/<int:comment_id>/upvotes', methods=['POST'])
    def post(self, user_id: int, comment_id: int):
        comment: ProjectComment = self.session.query(ProjectComment).filter(ProjectComment.id == comment_id).one()
        comment.upvote(user_id)

        return '', 200

    @user_required
    @route('/comments/<int:comment_id>/upvotes', methods=['DELETE'])
    def delete(self, user_id: int, comment_id: int):
        comment: ProjectComment = self.session.query(ProjectComment).filter(ProjectComment.id == comment_id).one()
        comment.annul_vote(user_id)

        return '', 200
