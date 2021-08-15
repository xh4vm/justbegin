from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TIMESTAMP, Column, Integer
from sqlalchemy.orm.scoping import scoped_session

db = SQLAlchemy()

class Model(db.Model):
    session: scoped_session = db.session

    id: int = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)
