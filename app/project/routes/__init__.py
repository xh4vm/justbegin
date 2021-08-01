from app import db, socketio
from app.decorators import request_is_json
from flask import json, render_template, request, jsonify, redirect, current_app
from flask_classy import FlaskView, route
from app.project import bp
from app.project.responses import ProjectResponses
from app.decorators import check_auth
from app.project.decorators import verify_authorship
from app.models import Project, User, FavoriteProject
from app.auth.utils import get_auth_instance
from sqlalchemy.sql.functions import func 


class Project(FlaskView):

    def get(self):
        id, claims = get_auth_instance().get_current_user_data_from_token()
        per_page, page = 20, request.args.get('page', 1, type=int)

        projects = Project.query.with_entities(Project).order_by(db.desc(Project.create_at))\
            .paginate(page, per_page)

        return render_template('project/index.html', projects=projects, user=claims)

    @check_auth
    @route('/create/', methods=['GET'])
    def create():
        id, claims = get_auth_instance().get_current_user_data_from_token()
        return render_template('project/creator.html', user=claims), 200

    @route('/<int:project_id>/')
    def get_project(self, project_id):
        id, claims = get_auth_instance().get_current_user_data_from_token()

        project = Project.query.get(project_id)
        return render_template('project/index.html', project=project, user=claims)

    @check_auth
    @request_is_json(error_message=ProjectResponses.BAD_DATA_TYPE, error_code=400)
    @route('/like/', methods=['POST'])
    def like(self):
        id, claims = get_auth_instance().get_current_user_data_from_token()
        project_id = request.json.get('project_id')

        project = Project.query.get(project_id)

        if project is None:
            return jsonify(ProjectResponses.BAD_PROJECT_ID_DATA), 400

        liked_project = FavoriteProject(user_id=id, project_id=project_id)

        try:
            db.session.add(liked_project)
            active = True
        except:
            db.session.delete(
                FavoriteProject.query.get((liked_project.user_id, liked_project.project_id)))
            active = False

        db.session.commit()

        return jsonify({"status": "success", "count": len(project.favorites), "active": active}), 200

    @route('/status_favorites/', methods=['POST'])
    def status_favorites(self):
        projects = Project.query.with_entities(Project.id, func.count(FavoriteProject.project_id).label('count'))\
            .filter(Project.id == FavoriteProject.project_id)\
            .group_by(FavoriteProject.project_id).all()

        return jsonify({"status": "success", "projects": projects}), 200

    @check_auth
    @request_is_json(error_message=ProjectResponses.BAD_DATA_TYPE, error_code=400)
    @verify_authorship(request_key='project_id')
    @route('/remove/', methods=['POST'])
    def remove():
        project_id = request.json.get('project_id')
        project = Project.query.get(project_id)

        if project is None:
            return jsonify(ProjectResponses.BAD_PROJECT_ID_DATA), 400

        db.session.delete(project)
        db.session.commit()

        return jsonify({'status': 'success', 'text': f'Проект {project.title} был успешно удален.'})

Project.register(bp)
