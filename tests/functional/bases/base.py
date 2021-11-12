from app.project.models import Project, create_author_project
from flask_testing import TestCase
from sqlalchemy.orm.scoping import scoped_session

from app import create_app, redis_client
from app.db import db
from config import TestConfig


class BaseTestCase(TestCase):
    session: scoped_session = db.session

    def create_app(self): 
        return create_app(TestConfig)
        
    def setUp(self):  
        db.create_all()
        db.session.commit()

    def tearDown(self): 
        db.session.remove()
        db.drop_all()
        redis_client.flushdb()
