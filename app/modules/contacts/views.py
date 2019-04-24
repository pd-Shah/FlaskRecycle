from flask import (
    Blueprint,
    redirect,
    render_template,
    session,
)
from flask_login import login_required

from .logic import *
from .forms import FormMessage, FormContact
from app.models import CHOICES_STATUS, CHOICES_PRIORITY
from app.modules.comments import FormComment
from app.snippets import COUNTRIES


contacts = Blueprint('contacts', __name__,
                     template_folder='templates')


task_status_dict = dict(CHOICES_STATUS)
task_priority_dict = dict(CHOICES_PRIORITY)


# LIST
@contacts.route("/")
@login_required
def index():
    # Contacts not implemented, fallback to list followers only
    followed_users = get_followed_users(user_id=session["user_id"])
    return render_template('contacts/index.html',
                           followed_users=followed_users,
                           countries=dict(COUNTRIES)
                           )


# VIEW
@contacts.route("/view/<contact_id>")
@login_required
def view(contact_id):
    form_comment = FormComment()
    contact = get_contact(contact_id)
    tasks = get_contact_related_tasks(contact)
    return render_template('contacts/view.html',
                           contact=contact,
                           tasks=tasks,
                           status_dict=task_status_dict,
                           priority_dict=task_priority_dict,
                           form_comment=form_comment
                           )


# MESSAGE
@contacts.route("/view/<contact_id>/message")
@login_required
def message(contact_id):
    form_message = FormMessage()
    contact = get_contact(contact_id)
    return render_template('contacts/message.html',
                           form_message=form_message,
                           contact=contact
                           )


# ADD
@contacts.route("/add", methods=('GET', 'POST'))
@login_required
def add():
    form_contact = FormContact()
    if form_contact.validate_on_submit():
        add_contact(form_contact)
        return redirect('/account/contacts/')
    return render_template('contacts/add.html',
                           form_contact=form_contact
                           )
