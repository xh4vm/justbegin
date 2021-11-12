from app.db import Model, ModelId
from sqlalchemy.sql.functions import func

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import BigInteger, SmallInteger, String, Integer


class Teammate(Model):
    
    ADMIN = 100601
    EDITOR = 2
    REVIEWER = 3
    INVESTOR = 4

    __table_args__ = (
        UniqueConstraint('user_id', 'project_id', 'role_id', name='uq_team_worker'),
    )

    user_id = Column(ModelId, ForeignKey('users.id'))
    project_id = Column(ModelId, ForeignKey('projects.id'))
    role_id = Column(SmallInteger)
    
    def __init__(self, user_id : int, project_id : int, role_id : int):
        self.user_id = user_id
        self.project_id = project_id
        self.role_id = role_id
