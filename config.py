import os
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    SECRET_KEY = 'gwkghkf2934ysfljb45efsjfhkadslg2'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db:5432/justbegin'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = 'gwkghkf2934ysfljb45efsjfhkadslg212askjdqrdfh124'
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)

    UPLOADS_DEFAULT_DEST = f'{basedir}/app/static/users'

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


class TestConfig(object):
    DEBUG = False
    SECRET_KEY = 'gwkghkf2934ysfljb45efsjfhkadslg2'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///' + os.path.join(basedir, "test_app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = 'gwkghkf2934ysfljb45efsjfhkadslg212askjdqrdfh124'
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)

    UPLOADS_DEFAULT_DEST = f'{basedir}/app/static/users'

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
