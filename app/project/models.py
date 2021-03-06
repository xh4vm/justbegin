from werkzeug.exceptions import abort
from ..user.auth.utils import get_auth_instance
from sqlalchemy.event.api import listens_for
from .teammate.models import Teammate
from sqlalchemy.sql.functions import func
from typing import List

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.sql.sqltypes import String, Integer

from .comment.models import ProjectComment
from .follower.models import ProjectFollower
from .story.exceptions import InvalidProjectStoryAuthorRole
from .story.models import ProjectStory
from ..db import Model
from app.user.models import User


class Project(Model):

    title: str = Column(String(128), nullable=False)
    description: str = Column(String, nullable=False)
    website: str = Column(String(1024), nullable=True)

    comments = relationship('ProjectComment')
    stories = relationship('ProjectStory', order_by='ProjectStory.created_at.desc()')

    def __init__(self, title: str, description: str, website: str = None) -> None:
        self.title = title
        self.description = description
        self.website = website

    def _set_like(self, user_id : int) -> bool:
        self.session.add(
            ProjectLike(user_id=user_id, project_id=self.id))
        self.session.commit()
        return True

    def _unset_like(self, user_id : int) -> bool:
        self.session.delete(ProjectLike.query.filter_by(user_id=user_id, project_id=self.id).first())
        self.session.commit()
        return False

    def like(self, user_id : int) -> bool:
        check_liked_project = ProjectLike.query.filter_by(user_id=user_id, project_id=self.id).first()
        return self._set_like(user_id) if check_liked_project is None else self._unset_like(user_id)

    def get_count_likes(self):
        favorites = self.session.query(func.count(ProjectLike.project_id).label('count'))\
            .group_by(ProjectLike.project_id).first()

        return favorites.count if favorites is not None else 0

    @property
    def parentless_comments(self) -> List[ProjectComment]:
        return (self.session
                    .query(ProjectComment)
                    .filter(ProjectComment.project_id == self.id, ProjectComment.parent_comment_id == None)
                    .order_by(ProjectComment.created_at)
                    .all())

    def leave_comment(self, author: User, content: str, parent_comment_id: int = None) -> ProjectComment:
        comment = ProjectComment(self.id, author.id, content, parent_comment_id)
        self.session.add(comment)
        self.session.commit()

        return comment

    def publish_story(self, author: User, title: str, content: str) -> ProjectStory:
        # TODO: Check user team role.
        if False:
            raise InvalidProjectStoryAuthorRole

        story = ProjectStory(self.id, author.id, title, content)
        self.session.add(story)
        self.session.commit()

        return story

    def follow(self, user: User) -> None:
        follower = (ProjectFollower.query
                    .filter(ProjectFollower.user_id == user.id, ProjectFollower.project_id == self.id)
                    .first())

        if follower is not None:
            return

        self.session.add(ProjectFollower(user.id, self.id))
        self.session.commit()

    def unfollow(self, user: User) -> None:
        follower = (ProjectFollower.query
                    .filter(ProjectFollower.user_id == user.id, ProjectFollower.project_id == self.id)
                    .first())

        if follower is not None:
            self.session.delete(follower)
            self.session.commit()

    def add_teammate(self, user_id : int, role_ids : list) -> None:
        for role_id in role_ids:
            teammate : Teammate = Teammate(user_id=user_id, project_id=self.id, role_id=role_id)
            self.session.add(teammate)
        
        self.session.commit()

    def delete_teammate(self, user_id : int) -> None:
        Teammate.query.filter_by(user_id=user_id, project_id=self.id).delete()
        self.session.commit()

    def delete_teammate_role(self, user_id : int, role_id : int) -> None:
        Teammate.query \
            .filter_by(user_id=user_id, project_id=self.id, role_id=role_id) \
            .delete()
        self.session.commit()


class ProjectLike(Model):

    __table_args__ = (
        UniqueConstraint('user_id', 'project_id', name='uq_project_like'),
    )

    user_id : int = Column(Integer, ForeignKey('users.id'), nullable=False)
    project_id : int = Column(Integer, ForeignKey('projects.id'), nullable=False)

@listens_for(Project, 'after_insert', named=True)
def create_author_project(mapper, connection, target):
    
    auth_data = get_auth_instance().get_current_user_data_from_token()

    if auth_data is None:
        abort(401)
        
    connection.execute(Teammate.__table__.insert() \
        .values(user_id=auth_data[0], project_id=target.id, role_id=Teammate.ADMIN))

