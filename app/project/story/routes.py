from flask import jsonify
from flask_classy import FlaskView, route
from sqlalchemy.orm.scoping import scoped_session

from .exceptions import InvalidProjectStoryAuthorRole
from .models import ProjectStory
from .schemas import post_project_story_schema, put_project_story_schema
from ..decorators import project_required, project_story_required, project_story_authorship_required
from ..models import Project
from ..serializers import serialize_project_story
from ...auth.decorators import user_required
from ...db import db
from ...decorators import request_validation_required
from ...models import User


class ProjectStories(FlaskView):
    session: scoped_session = db.session

    @project_required
    @route('/<int:project_id>/stories', methods=['GET'])
    def index(self, project: Project) -> tuple:
        return jsonify(list(map(serialize_project_story, project.stories))), 200

    @user_required
    @project_required
    @request_validation_required(post_project_story_schema)
    @route('/<int:project_id>/stories', methods=['POST'])
    def post(self, project: Project, user: User, validated_request: dict) -> tuple:
        try:
            story = project.publish_story(user, validated_request['title'], validated_request['content'])
        except InvalidProjectStoryAuthorRole:
            return jsonify(), 403

        return jsonify({'id': story.id}), 200

    @project_story_required
    @route('/stories/<int:story_id>', methods=['GET'])
    def get(self, story: ProjectStory) -> tuple:
        return jsonify(serialize_project_story(story)), 200

    @project_story_authorship_required
    @request_validation_required(put_project_story_schema)
    @route('/stories/<int:story_id>', methods=['PUT'])
    def put(self, story: ProjectStory, validated_request: dict) -> tuple:
        new_content = validated_request.get('content')
        new_title = validated_request.get('title')

        if new_title is not None:
            story.title = new_title

        if new_content is not None:
            story.content = new_content

        self.session.commit()

        return jsonify({'id': story.id}), 200

    @project_story_authorship_required
    @route('/stories/<int:story_id>', methods=['DELETE'])
    def delete(self, story: ProjectStory) -> tuple:
        self.session.delete(story)
        self.session.commit()

        return jsonify({'id': story.id}), 200
