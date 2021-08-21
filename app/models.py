from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db, jwt




class ProjectCreator(db.Model):
    __tablename__ = 'project_creator'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)

class ProjectBlog(db.Model):
    __tablename__ = "project_blog"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    title = db.Column(db.String(128), nullable=False)
    about = db.Column(db.String(512), nullable=False)
    description = db.Column(db.String(6144), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


'''
class Project(db.Model):
    __tablename__ = "projects"
    # __table_args__ = (
    #     db.CheckConstraint(re.match('https?://[^$]+', website_link, re.IGNORECASE)),
    #     db.CheckConstraint(re.match('https://github\.com/[^$]+', repo_link, re.IGNORECASE)),
    # )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    about = db.Column(db.String(512), nullable=False)
    description = db.Column(db.String(6144), nullable=False)
    image = db.Column(db.String(512), nullable=True)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    website_link = db.Column(db.String(1024), nullable=True)
    repo_link = db.Column(db.String(1024), nullable=True)

    comments = db.relationship('ProjectComment')

    categories = db.relationship('Category', secondary='project_category', backref=db.backref('projects'))
    authors = db.relationship('User', secondary='project_creator', backref=db.backref('projects'))
    favorites = db.relationship('User', secondary='favorite_project', backref=db.backref('favorite_projects'))
'''
