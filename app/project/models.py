from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from ..db import Model


class Project(Model):

    title: str = Column(String(128), nullable=False)
    description: str = Column(String, nullable=False)
    website: str = Column(String(1024), nullable=True)

    comments = relationship('ProjectComment')

    def __init__(self, title: str, description: str, website: str = None) -> None:
        self.title = title
        self.description = description
        self.website = website
