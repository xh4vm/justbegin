from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db, jwt


class User(db.Model):
    __tablename__ = "users"
    # __table_args__ = (
    #     db.CheckConstraint(re.match('[^@]+@[^\.]+[^$]+', email, re.IGNORECASE)),
    # )

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(128), nullable=False, unique=True)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(128), nullable=True)
    telegram_nickname = db.Column(db.String(32), nullable=False, unique=True)

    def __init__(self, nickname, email, password, telegram_nickname, avatar=None, first_name=None, last_name=None):
        self.nickname = nickname
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.avatar = avatar
        self.telegram_nickname = telegram_nickname

    @staticmethod
    def create_password_hash(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def contains_with_email(email):
        user = User.query.with_entities(User.email).filter_by(email=email).first()
        return False if user is None else True

    @staticmethod
    @jwt.user_claims_loader
    def add_claims(user):
        return {
            'email': user.email,
            'nickname': user.nickname,
            'avatar': user.avatar,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'telegram_nickname': user.telegram_nickname
        }

    @staticmethod
    @jwt.user_identity_loader
    def add_identity(user):
        return user.id

class FavoriteProject(db.Model):
    __tablename__ = "favorite_project"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)

class ProjectCreator(db.Model):
    __tablename__ = 'project_creator'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)

class ProjectWorker(db.Model):
    __tablename__ = 'project_worker'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)

class ProjectStar(db.Model):
    __tablename__ = 'project_star'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False, unique=True)

class ProjectCategory(db.Model):
    __tablename__ = "project_category"

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)

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
