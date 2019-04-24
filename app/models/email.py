from flask_babel import lazy_gettext
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired

from app import db
from ._mixin import TimestampMixin, AuthorMixin


class EmailOut(TimestampMixin, AuthorMixin, db.Model):
    __tablename__ = 'email_out'
    id = db.Column(db.Integer, primary_key=True)
    name_sender = db.Column(db.String(100))
    name_recipient = db.Column(
        db.String(100),
        info={'label': lazy_gettext('Recipient Name')})
    email_recipient = db.Column(
        db.String(100),
        info={'label': lazy_gettext('Recipient Email'),
              'validators': InputRequired()})
    subject = db.Column(
        db.String(100),
        info={'label': lazy_gettext('Subject'),
              'validators': InputRequired()})
    message = db.Column(
        db.String(100),
        info={'label': lazy_gettext('Message'),
              'widget': TextArea(),
              'validators': InputRequired()})
