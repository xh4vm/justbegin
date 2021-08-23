from .base import BaseTestCase
from app.project.models import Project, create_author_project
from sqlalchemy.event import remove, listen


class BaseWithoutCreateProjectAuthorTestCase(BaseTestCase):

    def setUp(self):  
        remove(Project, "after_insert", create_author_project)
        super().setUp()

    def tearDown(self): 
        super().tearDown()
        listen(Project, "after_insert", create_author_project)
