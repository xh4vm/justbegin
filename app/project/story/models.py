from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import String

from app.db import Model, ModelId
from app.models import User


class ProjectStory(Model):
    __tablename__ = 'project_stories'

    project_id: int = Column(ModelId, ForeignKey('projects.id'), nullable=False)
    author_user_id: int = Column(ModelId, ForeignKey('users.id'), nullable=False)
    title: str = Column(String, nullable=False)
    content: str = Column(String, nullable=False)

    author: User = relationship('User')

    def __init__(self, project_id: int, author_user_id: int, title: str, content: str) -> None:
        self.project_id = project_id
        self.author_user_id = author_user_id
        self.title = title
        self.content = content

    def update(self, title: str = None, content: str = None) -> None:
        need_commit = False

        if title is not None and self.title != title:
            self.title = title
            need_commit = True

        if content is not None and self.content != content:
            self.content = content
            need_commit = True

        if need_commit:
            self.session.commit()
