import os
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = '1b3a10657a23bdd02d5262f375d5255a045b6ccfca4082ecaf7b0c1efea3dfad'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://test:test@db/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = '1b3a10657a23bdd02d5262f375d5255a045b6ccfca4082ecaf7b0c1efea3dfad'
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)

    UPLOADS_DEFAULT_DEST = f'{basedir}/app/static/users'

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    AUTH_METHOD = 'JWTAuth'

class DeployConfig(BaseConfig):
    DEBUG = False

class Config(BaseConfig):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True

class TestConfig(BaseConfig):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///' + os.path.join(basedir, "test_app.db")
