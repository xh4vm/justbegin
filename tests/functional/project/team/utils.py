from app.project.team.models import Teammates
from app.db import db


def add_teammate_roles(user_id : int, project_id : int, teammate_role_ids : list) -> None:
    for teammate_role_id in teammate_role_ids:
        teammate : Teammates = Teammates(user_id=user_id, project_id=project_id, teammate_role_id=teammate_role_id)
        db.session.add(teammate)
        
    db.session.commit()