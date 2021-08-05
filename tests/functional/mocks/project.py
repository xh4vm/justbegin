from app import db
from app.models import Project


class ProjectMock:
    title = "Title"
    about = "About"
    description = "Description"

    @staticmethod
    def init():
        project = Project(title=ProjectMock.title, about=ProjectMock.about, description=ProjectMock.description)
        db.session.add(project)
        db.session.commit()
