from app.db import Model, ModelId
from sqlalchemy.sql.functions import func

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import BigInteger, String, Integer


class Teammates(Model):
    
    ROLES = {
        "Administrator": 1,
        "Editor": 2,
        "Reviewer": 3,
        "Investor": 4,
        
    }

    __table_args__ = (
        UniqueConstraint('user_id', 'project_id', 'teammate_role_id', name='uq_team_worker'),
    )

    user_id = Column(ModelId, ForeignKey('users.id'))
    project_id = Column(ModelId, ForeignKey('projects.id'))
    teammate_role_id = Column(ModelId)
    
    def __init__(self, user_id : int, project_id : int, teammate_role_id : int):
        self.user_id = user_id
        self.project_id = project_id
        self.teammate_role_id = teammate_role_id

    @staticmethod
    def get_role_id(role_name="Administrator"):
        return Teammates.ROLES[role_name]
