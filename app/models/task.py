from flask_babel import lazy_gettext
from wtforms.widgets import TextArea, Select
from wtforms.validators import InputRequired
from sqlalchemy_utils import ChoiceType

from app import db
from app.models._mixin import TimestampMixin, AuthorMixin


CHOICES_EMPTY = [("", "---")]

CHOICES_PRIORITY = [("", lazy_gettext('Select Priority')),
                    (u'1', lazy_gettext('Later')),
                    (u'2', lazy_gettext('Low')),
                    (u'3', lazy_gettext('Normal')),
                    (u'4', lazy_gettext('High'))]

CHOICES_STATUS = [("", lazy_gettext('Select Priority')),
                  (u'1', lazy_gettext('New')),
                  (u'2', lazy_gettext('In Progress')),
                  (u'4', lazy_gettext('Waiting')),
                  (u'5', lazy_gettext('Under review')),
                  (u'6', lazy_gettext('Done')),
                  (u'8', lazy_gettext('Cancelled'))]


rel_users_tasks = db.Table('rel_users_tasks',
                            db.Column('user_id',
                                      db.Integer,
                                      db.ForeignKey('users.id'),
                                      nullable=False),
                            db.Column('task_id',
                                      db.Integer,
                                      db.ForeignKey('tasks.id'),
                                      nullable=False),
                            db.PrimaryKeyConstraint('user_id', 'task_id'))


rel_contacts_tasks = db.Table('rel_contacts_tasks',
                               db.Column('contact_id',
                                         db.Integer,
                                         db.ForeignKey('contacts.id'),
                                         nullable=False),
                               db.Column('task_id',
                                         db.Integer,
                                         db.ForeignKey('tasks.id'),
                                         nullable=False),
                               db.PrimaryKeyConstraint('contact_id', 'task_id'))


# https://seagullbird.xyz/posts/how-to-delete-many-to-many-in-sqlalchemy/

class Task(TimestampMixin, AuthorMixin, db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(
        db.String(120),
        info={'label': lazy_gettext('Summary'),
              'validators': InputRequired()})
    description = db.Column(
        db.String(1000),
        info={'label':
              'Description',
              'widget': TextArea()})
    due = db.Column(db.DateTime,
                    info={'label': lazy_gettext('Due')})
    priority = db.Column(
        ChoiceType(CHOICES_PRIORITY),
        info={'label': lazy_gettext('Priority')},
        nullable=False
    )
    status = db.Column(
        ChoiceType(CHOICES_STATUS),
        info={'label': lazy_gettext('Status')},
        nullable=False
    )
    assigned = db.relationship(
        'User',
        secondary=rel_users_tasks,
        backref='tasks',
        info={'choices': [],
              'label': lazy_gettext('Assigned User'),
              'widget': Select()}
    )
    _contacts = db.relationship(
        'Contact',
        secondary=rel_contacts_tasks,
        backref='contacts',
        info={'choices': [],
              'label': lazy_gettext('Related Contact'),
              'widget': Select()}
    )
    comments = db.relationship('Comment', backref='tasks', lazy=True)

    def add_user(self, user):
        self.assigned.append(user)

    def remove_user(self, user):
        self.assigned.remove(user)

    def add_contact(self, contact):
        self._contacts.append(contact)

    def remove_contact(self, contact):
        self._contacts.remove(contact)

    # TODO: Ensure that the contact isn't already assigned ('def has contact')
