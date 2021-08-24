from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy.sql.schema import Column
from ..db import Model
from app import jwt
from werkzeug.security import generate_password_hash, check_password_hash


class User(Model):

    id = Column(Integer, primary_key=True)
    nickname = Column(String(128), nullable=False, unique=True)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    avatar = Column(String(128), nullable=True)
    telegram_nickname = Column(String(32), nullable=False, unique=True)

    followed_project_stories = relationship('ProjectStory',
                                        secondary='join(Project, ProjectFollower,'
                                                    'Project.id == ProjectFollower.project_id)',
                                        order_by='ProjectStory.created_at.desc()',
                                        viewonly=True)

    projects_development = relationship('Project',
                                        secondary='join(Project, TeamWorker, '
                                                    'Project.id == TeamWorker.project_id)',
                                        secondaryjoin="User.id == TeamWorker.user_id",
                                        order_by='Project.created_at.desc()',
                                        viewonly=True)

    # project_roles = relationship('TeamWorker',
    #                             primaryjoin="User.id == TeamWorker.user_id",
    #                             order_by='TeamWorker.created_at.desc()',
    #                             viewonly=True)

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