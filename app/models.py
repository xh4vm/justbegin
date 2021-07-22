from app import db, jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re


class User(db.Model):
    __tablename__ = "user"
    __table_args__ = (
        db.CheckConstraint(re.match('[^@]+@[^\.]+[^$]+', email, re.IGNORECASE)),
    )

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(128), nullable=False, unique=True)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    avatar = db.Column(db.String(128), nullable=True)

    def __init__(self, nickname, email, password, avatar=None, first_name=None, last_name=None):
        self.nickname = nickname
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.avatar = avatar

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def check_email(self):
        user = User.query.with_entities(User.email).filter_by(email=self.email).first()
        return True if user is None else False

    @staticmethod
    @jwt.user_claims_loader
    def add_claims(user):
        return {
            'email': user.email,
            'nickname': user.nickname,
            'avatar': user.avatar,
            'first_name': user.first_name,
            'last_name': user.last_name
        }

    @staticmethod
    @jwt.user_identity_loader
    def add_identity(user):
        return user.id
