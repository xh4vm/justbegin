from app import db, jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(128), nullable=False, default='')
    last_name = db.Column(db.String(128), nullable=False, default='')
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    image = db.Column(db.String(128))

    def __init__(self, nickname, email, password, image=None, first_name=None, last_name=None):
        self.nickname = nickname
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.image = image

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
            'avatar': user.image
        }

    @staticmethod
    @jwt.user_identity_loader
    def add_identity(user):
        return user.id

