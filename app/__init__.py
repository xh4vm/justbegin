from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from config import Config
from app.jinja_functions import *
from flask_redis import FlaskRedis
from celery import Celery


db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()
jwt = JWTManager()
redis_client = FlaskRedis()
celery = Celery(__name__, backend=Config.CELERY_RESULT_BACKEND, broker=Config.CELERY_BROKER_URL)

def register_blueprints(app):
    from app.home import bp as home_bp
    app.register_blueprint(home_bp)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, message_queue="redis://")
    jwt.init_app(app)
    redis_client.init_app(app)

    register_blueprints(app)

    app.jinja_env.globals.update(randomword=randomword)

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
