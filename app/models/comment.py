from flask_babel import lazy_gettext
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired

from app import db
from ._mixin import TimestampMixin, AuthorMixin


class Comment(TimestampMixin, AuthorMixin, db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000), info={'label': lazy_gettext('Comment'),
                                               'widget': TextArea(),
                                               'validators': InputRequired()})
    _task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
