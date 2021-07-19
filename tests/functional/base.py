from config import TestConfig
from flask_testing import TestCase
from app import create_app, db, redis_client


class BaseTestCase(TestCase):

    def create_app(self): 
        return create_app(TestConfig)
        
    def setUp(self):  
        db.create_all()
        db.session.commit()

    def tearDown(self): 
        db.session.remove()
        db.drop_all()
        redis_client.flushdb()