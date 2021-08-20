from sqlalchemy import Column, ForeignKey, UniqueConstraint

from ...db import Model, ModelId


class ProjectFollower(Model):

    __table_args__ = (
        UniqueConstraint('user_id', 'project_id'),
    )

    user_id: int = Column(ModelId, ForeignKey('users.id'), nullable=False)
    project_id: int = Column(ModelId, ForeignKey('projects.id'), nullable=False)

    def __init__(self, user_id: int, project_id: int) -> None:
        self.user_id = user_id
        self.project_id = project_id
