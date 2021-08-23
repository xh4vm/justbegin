from app.db import BaseModel, Model, ModelId
from sqlalchemy.sql.functions import func

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import BigInteger, String, Integer


class TeamWorker(Model):
    
    __table_args__ = (
        UniqueConstraint('user_id', 'project_id', 'worker_role_id', name='uq_team_worker'),
    )

    user_id = Column(ModelId, ForeignKey('users.id'))
    project_id = Column(ModelId, ForeignKey('projects.id'))
    worker_role_id = Column(ModelId, ForeignKey('worker_roles.id'))
    
    def __init__(self, user_id : int, project_id : int, worker_role_id : int):
        self.user_id = user_id
        self.project_id = project_id
        self.worker_role_id = worker_role_id
        

class WorkerRole(Model):
    __admin_name__ = "Administrator"

    name = Column(String(128), unique=True)

    def __init__(self, name : str):
        self.name = name

    @staticmethod
    def get_admin():
        return WorkerRole.query.filter_by(name=WorkerRole.__admin_name__).first()
