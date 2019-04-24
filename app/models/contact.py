from flask_babel import lazy_gettext
from wtforms.widgets import TextArea
from ._mixin import TimestampMixin, AuthorMixin

from app import db


class Contact(TimestampMixin, AuthorMixin, db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), info={'label': lazy_gettext('First Name')})
    last_name = db.Column(db.String(100), info={'label': lazy_gettext('Last Name')})
    organisation = db.Column(db.String(100), info={'label': lazy_gettext('Organisation')})
    title = db.Column(db.String(100), info={'label': lazy_gettext('Title')})
    email = db.Column(db.String(100), info={'label': lazy_gettext('EMail')})
    phone = db.Column(db.String(100), info={'label': lazy_gettext('Phone')})
    mobile = db.Column(db.String(100), info={'label': lazy_gettext('Mobile')})
    description = db.Column(db.String(100), info={'label': lazy_gettext('Description'), 'widget': TextArea()})
