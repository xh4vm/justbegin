from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.sql.functions import sum, coalesce
from sqlalchemy.sql.sqltypes import String, Integer

from .exceptions import UnexpectedProjectRelation
from ...db import Model
from ...models import User


class ProjectComment(Model):
    project_id: int = Column(Integer, ForeignKey('projects.id'), nullable=False)
    author_user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    content: str = Column(String, nullable=False)
    parent_comment_id: int = Column(Integer, ForeignKey('project_comments.id'), nullable=True)

    author: User = relationship('User')
    replies = relationship('ProjectComment', order_by='ProjectComment.created_at')

    __score = None

    def __init__(self, project_id: int, author_user_id: int, content: str, parent_comment_id: int = None) -> None:
        if parent_comment_id is not None:
            parent = self.session.query(self.__class__).filter(self.__class__.id == parent_comment_id).one()

            if parent.project_id != project_id:
                raise UnexpectedProjectRelation('The parent comment must belong to the same project as the child')

        self.project_id = project_id
        self.author_user_id = author_user_id
        self.content = content
        self.parent_comment_id = parent_comment_id

    @property
    def score(self) -> int:
        if self.__score is None:
            self.__score = (self.session
                            .query(coalesce(sum(ProjectCommentVote.value), 0))
                            .filter(ProjectCommentVote.comment_id == self.id)
                            .scalar())

        return self.__score

    def upvote(self, user_id: int) -> None:
        ProjectCommentVote.upsert(self.session, self.id, user_id, 1)

    def annul_vote(self, user_id: int) -> None:
        ProjectCommentVote.upsert(self.session, self.id, user_id, 0)


class ProjectCommentVote(Model):
    __table_args__ = (
        UniqueConstraint('comment_id', 'user_id', name='single_vote_per_user'),
    )

    comment_id: int = Column(Integer, ForeignKey('project_comments.id', ondelete='CASCADE'), nullable=False)
    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    value: int = Column(Integer, nullable=False)

    def __init__(self, project_comment_id: int, user_id: int, value: int) -> None:
        self.comment_id = project_comment_id
        self.user_id = user_id
        self.value = value

    @classmethod
    def upsert(cls, session: scoped_session, project_comment_id: int, user_id: int, value: int) -> None:
        vote: ProjectCommentVote = (session
                                    .query(ProjectCommentVote)
                                    .filter(ProjectCommentVote.comment_id == project_comment_id,
                                            ProjectCommentVote.user_id == user_id)
                                    .first())

        if vote is None:
            vote = ProjectCommentVote(project_comment_id, user_id, value)
            session.add(vote)
        else:
            vote.value = value

        session.commit()
