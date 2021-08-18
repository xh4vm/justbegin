from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer

from ..db import Model, BaseModel


class Project(Model):

    title: str = Column(String(128), nullable=False)
    description: str = Column(String, nullable=False)
    website: str = Column(String(1024), nullable=True)

    comments = relationship('ProjectComment')

    def __init__(self, title: str, description: str, website: str = None) -> None:
        self.title = title
        self.description = description
        self.website = website

class FavoriteProject(BaseModel):

    user_id : int = Column(Integer, ForeignKey('users.id'), primary_key=True)
    project_id : int = Column(Integer, ForeignKey('projects.id'), primary_key=True)