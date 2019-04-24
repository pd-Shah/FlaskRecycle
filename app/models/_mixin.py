from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr

from .. import db


class TimestampMixin(object):
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)


class AuthorMixin(object):

    @declared_attr
    def author_id(cls):
        return db.Column(db.Integer, db.ForeignKey('users.id'))

    def author(cls):
        return db.relationship("User")











