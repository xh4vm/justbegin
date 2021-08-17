from datetime import datetime
import re

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TIMESTAMP, Column, BigInteger
from sqlalchemy.ext.declarative.api import declared_attr
from sqlalchemy.orm.scoping import scoped_session

db = SQLAlchemy()


class Model(db.Model):
    __abstract__ = True

    session: scoped_session = db.session

    id: int = Column(BigInteger, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    @declared_attr
    def __tablename__(cls):
        return re.sub('(?!^)([A-Z][a-z]+)', r'_\1', cls.__name__).lower() + 's'

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)
