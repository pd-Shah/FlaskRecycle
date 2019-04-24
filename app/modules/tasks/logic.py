from flask import flash, json
from flask_babel import gettext
from flask_login import current_user
from app.models import Task, Contact
from app.account import get_user
from app import db


def search_tasks(data):
    data = json.loads(data)

    if 'search' in data.keys():

        result = {}

        if 'keyword' in data.keys():
            result = Task.query.filter(Task.summary.like('%' + data['keyword'] + '%'))
        if 'status' in data.keys():
            result = Task.query.filter_by(status=(data['status'])).all()
        if 'priority' in data.keys():
            result = Task.query.filter_by(priority=(data['priority'])).all()
        flash("Search results for {}".format(data))

        return result

    else:

        return {}


def get_task(_id):
    result = Task.query.get(_id)
    return result


def get_tasks(status, operation):
    if status is not None and operation == 'not':
        result = Task.query.filter(Task.status != status).all()
    elif status is not None:
        result = Task.query.filter(Task.status == status).all()
    else:
        result = Task.query.all()
    return result


def save_task(data, contact_id):
    new_task = Task(
        summary=data.summary.data,
        description=data.description.data,
        due=data.due.data,
        priority=str(data.priority.data),
        status=str(data.status.data),
        author_id=current_user.id
    )
    if contact_id is not None:
        contact = Contact.query.get(contact_id)
        new_task.add_contact(contact)
        flash(gettext(
            'Contact {} associated with Task'.format(contact.email)))
    db.session.add(new_task)
    db.session.commit()
    return 'success'


def update_task(data, _id):
    task = Task.query.get(_id)
    task.summary = data.summary.data
    task.description = data.description.data
    task.due = data.due.data
    task.priority = str(data.priority.data)
    task.status = str(data.status.data)
    db.session.commit()
    flash(gettext('Task has been updated'))
    return 'success'


def relate_task(task_id, type, type_id):
    task = Task.query.get(task_id)
    if type == 'contact':
        contact = Contact.query.get(type_id)
        task._contacts.append(contact)
        flash(gettext('{} related to task'.format(contact.email)))
    elif type == 'user':
        user = get_user(type_id)
        task.assigned.append(user)
        flash(gettext('{} related to task'.format(user.email)))
    return 'success'


def relate_task_remove(task_id, type, type_id):
    task = Task.query.get(task_id)
    if type == 'contact':
        contact = Contact.query.get(type_id)
        task._contacts.remove(contact)
        flash(gettext('{} removed from task'.format(contact.email)))
    elif type == 'user':
        user = get_user(type_id)
        task.assigned.remove(user)
        flash(gettext('{} removed from task'.format(user.email)))
    db.session.commit()
    return 'success'


def delete_task(task_id):
    task = Task.query.get(task_id)
    task.assigned.clear()
    task._contacts.clear()
    task.comments.clear()
    db.session.delete(task)
    db.session.commit()
    return 'success'
