from sqlalchemy.sql.functions import func
from .comment.models import ProjectComment
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer

from ..db import Model, BaseModel


class Project(Model):

    title: str = Column(String(128), nullable=False)
    description: str = Column(String, nullable=False)
    website: str = Column(String(1024), nullable=True)

    comments : ProjectComment = relationship('ProjectComment')

    def __init__(self, title: str, description: str, website: str = None) -> None:
        self.title = title
        self.description = description
        self.website = website

    def _set_like(self, user_id : int) -> bool:
        self.session.add(
            FavoriteProject(user_id=user_id, project_id=self.id))
        self.session.commit()
        return True

    def _unset_like(self, user_id : int) -> bool:
        self.session.delete(FavoriteProject.query.get((user_id, self.id)))
        self.session.commit()
        return False

    def like(self, user_id : int) -> bool:
        check_liked_project = FavoriteProject.query.get((user_id, self.id))
        return self._set_like(user_id) if check_liked_project is None else self._unset_like(user_id)

    def get_count_likes(self):
        favorites = self.session.query(func.count(FavoriteProject.project_id).label('count'))\
            .group_by(FavoriteProject.project_id).first()
            
        return favorites.count if favorites is not None else 0

class FavoriteProject(BaseModel):

    user_id : int = Column(Integer, ForeignKey('users.id'), primary_key=True)
    project_id : int = Column(Integer, ForeignKey('projects.id'), primary_key=True)