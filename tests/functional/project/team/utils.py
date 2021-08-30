from app.project.team.models import WorkerRole, Teammates
from app.db import db


def add_team_worker_roles(user_id : int, project_id : int, worker_role_ids : list) -> None:
    for worker_role_id in worker_role_ids:
        team_worker : Teammates = Teammates(user_id=user_id, project_id=project_id, worker_role_id=worker_role_id)
        db.session.add(team_worker)
        
    db.session.commit()