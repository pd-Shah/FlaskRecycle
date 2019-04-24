from flask_babel import lazy_gettext
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired

from app import db
from ._mixin import TimestampMixin, AuthorMixin

from app.models import User


rel_conversations_users = db.Table('rel_conversations_users',
                                   db.Column('user_id',
                                             db.Integer,
                                             db.ForeignKey('users.id'),
                                             nullable=False),
                                   db.Column('conversation_id',
                                             db.Integer,
                                             db.ForeignKey('conversations.id'),
                                             nullable=False),
                                   db.PrimaryKeyConstraint('user_id',
                                                           'conversation_id'))


class Conversation(TimestampMixin, AuthorMixin, db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(250),
                        info={'label': lazy_gettext('Subject')})
    _offer_id = db.Column(db.Integer, db.ForeignKey('offers.id'))
    offer = db.relationship(
        'Offer',
        backref='offer'
    )
    _messages = db.relationship(
        'Message',
        backref='messages'
    )
    _recipients = db.relationship(
        'User',
        secondary=rel_conversations_users,
        backref='conversations'
    )


class Message(TimestampMixin, AuthorMixin, db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000),
                        info={'label': lazy_gettext('Message'),
                              'widget': TextArea(),
                              'validators': InputRequired()})
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'))
