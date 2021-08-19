from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.event import listens_for
from sqlalchemy.orm import relationship
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.sql.functions import sum, coalesce
from sqlalchemy.sql.sqltypes import String, SmallInteger

from .exceptions import UnexpectedProjectRelation, InvalidProjectCommentVoteValue, OwnCommentVoting
from ...db import Model, ModelId
from ...models import User


class ProjectComment(Model):
    project_id: int = Column(ModelId, ForeignKey('projects.id'), nullable=False)
    author_user_id: int = Column(ModelId, ForeignKey('users.id'), nullable=False)
    content: str = Column(String, nullable=False)
    parent_comment_id: int = Column(ModelId, ForeignKey('project_comments.id'), nullable=True)

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

    def __vote(self, user_id: int, value: int) -> None:
        if user_id == self.author_user_id:
            raise OwnCommentVoting

        ProjectCommentVote.upsert(self.session, self.id, user_id, value)

    def upvote(self, user_id: int) -> None:
        self.__vote(user_id, ProjectCommentVote.UPVOTE)

    def downvote(self, user_id: int) -> None:
        self.__vote(user_id, ProjectCommentVote.DOWNVOTE)

    def annul_vote(self, user_id: int) -> None:
        self.__vote(user_id, ProjectCommentVote.ANNUL)


class ProjectCommentVote(Model):
    UPVOTE: int = 1
    DOWNVOTE: int = -1
    ANNUL: int = 0

    __table_args__ = (
        UniqueConstraint('comment_id', 'user_id', name='single_vote_per_user'),
    )

    comment_id: int = Column(ModelId, ForeignKey('project_comments.id', ondelete='CASCADE'), nullable=False)
    user_id: int = Column(ModelId, ForeignKey('users.id'), nullable=False)
    value: int = Column(SmallInteger, nullable=False)

    def __init__(self, project_comment_id: int, user_id: int, value: int) -> None:
        self.comment_id = project_comment_id
        self.user_id = user_id
        self.value = value

    @classmethod
    def upsert(cls, session: scoped_session, comment_id: int, user_id: int, value: int) -> None:
        vote = (session
                .query(ProjectCommentVote)
                .filter(ProjectCommentVote.comment_id == comment_id,
                        ProjectCommentVote.user_id == user_id)
                .first())

        if vote is None:
            vote = ProjectCommentVote(comment_id, user_id, value)
            session.add(vote)
        else:
            vote.value = value

        session.commit()


@listens_for(ProjectCommentVote, 'before_insert', named=True)
@listens_for(ProjectCommentVote, 'before_update', named=True)
def validate_project_comment_vote_value(**kwargs):
    if kwargs['target'].value not in (ProjectCommentVote.UPVOTE, ProjectCommentVote.DOWNVOTE, ProjectCommentVote.ANNUL):
        raise InvalidProjectCommentVoteValue
