from flask import flash
from flask_babel import gettext
from flask_login import current_user
from app.models import Contact, Task, User
from app import db


def get_contact(contact_id):
    result = Contact.query.get(contact_id)
    return result


def get_contacts(user_id):
    return None


def get_followed_users(user_id):
    user = User.query.get(user_id)
    result = user.followed_users()
    return result


def add_contact(data):
    contact = Contact(
        first_name=data.first_name.data,
        last_name=data.last_name.data,
        organisation=data.organisation.data,
        title=data.title.data,
        email=data.email.data,
        phone=data.phone.data,
        mobile=data.mobile.data,
        description=data.description.data,
        author_id=current_user.id
    )
    db.session.add(contact)
    db.session.commit()
    flash(gettext('A new contact has been added.'))
    return 'success'


def get_contact_related_tasks(contact):
    result = Task.query.with_parent(contact)
    return result
