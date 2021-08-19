from flask import request, jsonify
from flask_classy import FlaskView, route
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.sql.functions import func

from app import db
from app.auth.decorators import check_auth
from app.auth.utils import get_auth_instance
from app.decorators import request_is_json, request_validation_required
from app.project.models import FavoriteProject
from app.project.decorators import verify_authorship
from app.project.responses import ProjectResponses
from .models import Project
from .serializers import serialize_project
from .schemas import post_like_schema


class Projects(FlaskView):

    session: scoped_session = db.session

    def index(self):
        projects = (self.session
                    .query(Project)
                    .order_by(Project.created_at)
                    .all())

        return jsonify(list(map(serialize_project, projects))), 200

    @check_auth
    def post(self):
        project = Project(request.form['title'], request.form['description'], request.form['website'])
        self.session.add(project)
        self.session.commit()

        return jsonify({'id': project.id}), 200

    @route('/<int:project_id>/')
    def get_project(self, project_id):
        id, claims = get_auth_instance().get_current_user_data_from_token()

        project = Project.query.get(project_id)
        return "шаблон"

    @check_auth
    @route('/like/', methods=['POST'])
    @request_validation_required(post_like_schema)
    def like(self, validated_request: dict):
        id, claims = get_auth_instance().get_current_user_data_from_token()
        project_id = validated_request.get('project_id')

        project = Project.query.get(project_id)

        if project is None:
            return jsonify(ProjectResponses.BAD_PROJECT_ID_DATA), 400

        liked_project = FavoriteProject(user_id=id, project_id=project_id)
        check_liked_project = FavoriteProject.query.get((id, project_id))

        if check_liked_project is None:
            db.session.add(liked_project)
            active = True
        else:
            db.session.delete(
                FavoriteProject.query.get((liked_project.user_id, liked_project.project_id)))
            active = False

        db.session.commit()

        favorites = db.session.query(func.count(FavoriteProject.project_id).label('count'))\
            .group_by(FavoriteProject.project_id).first()

        return jsonify({"status": "success", "count": favorites.count if favorites is not None else 0, "active": active}), 200

    @route('/status_favorites/', methods=['POST'])
    def status_favorites(self):
        projects = Project.query.with_entities(Project.id, func.count(FavoriteProject.project_id).label('count'))\
            .filter(Project.id == FavoriteProject.project_id)\
            .group_by(FavoriteProject.project_id).all()

        return jsonify({"status": "success", "projects": projects}), 200

    @check_auth
    @verify_authorship(request_key='project_id')
    @route('/remove/', methods=['POST'])
    def remove(self):
        project_id = request.form.get('project_id')
        project = Project.query.get(project_id)

        if project is None:
            return jsonify(ProjectResponses.BAD_PROJECT_ID_DATA), 400

        db.session.delete(project)
        db.session.commit()

        right_response = ProjectResponses.SUCCESS_REMOVE.copy()
        right_response["message"] = right_response["message"].substitute(title=project.title)

        return jsonify(right_response), 200
