from random import randint

from app.db import db
from app.project.models import Project


def create_project(title: str = None, description: str = None, website: str = None) -> Project:
    project = Project(
        title or 'Test Project Title',
        description or 'Test project description.',
        website or 'test.project.com',
    )

    # Needed for compatibility between actual and test DB
    project.id = randint(1, 1000000)

    db.session.add(project)
    db.session.commit()

    return project
