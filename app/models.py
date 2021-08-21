from datetime import datetime

from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, jwt


class ProjectCreator(db.Model):
    __tablename__ = 'project_creator'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)

# class ProjectBlog(db.Model):
#     __tablename__ = "project_blog"

#     id = db.Column(db.Integer, primary_key=True)
#     project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
#     title = db.Column(db.String(128), nullable=False)
#     about = db.Column(db.String(512), nullable=False)
#     description = db.Column(db.String(6144), nullable=False)
#     create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

