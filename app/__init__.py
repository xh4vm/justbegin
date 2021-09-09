from celery import Celery
from config import Config
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_socketio import SocketIO

from .db import db

migrate = Migrate()
socketio = SocketIO()
jwt = JWTManager()
redis_client = FlaskRedis()
celery = Celery(__name__, backend=Config.CELERY_RESULT_BACKEND, broker=Config.CELERY_BROKER_URL)
mail = Mail()

def register_blueprints(app):
    from app.home import bp as home_bp
    app.register_blueprint(home_bp)

    from app.user import bp as user_bp
    app.register_blueprint(user_bp)

    from app.project import bp as project_bp
    app.register_blueprint(project_bp)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, message_queue="redis://")
    jwt.init_app(app)
    redis_client.init_app(app)
    mail.init_app(app)

    register_blueprints(app)

    app.app_context().push()

    return app

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
