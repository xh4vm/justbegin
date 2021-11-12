from app.project.teammate.models import Teammate
from app.db import db


def add_teammate_roles(user_id : int, project_id : int, role_ids : list) -> None:
    for role_id in role_ids:
        teammate : Teammate = Teammate(user_id=user_id, project_id=project_id, role_id=role_id)
        db.session.add(teammate)
        
    db.session.commit()