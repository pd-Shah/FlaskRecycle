from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    json
)
from flask_babel import gettext
from flask_login import login_required
from .forms import *
from .logic import *

from app.account import get_users
from app.models import CHOICES_STATUS, CHOICES_PRIORITY
from app.modules.statistics import inject_user_sidebar_stats
from app.modules.comments import FormComment, save_comment, get_comments
from app.modules.contacts import get_contact, get_contacts


tasks = Blueprint('tasks', __name__,
                  template_folder='templates')


status_dict = dict(CHOICES_STATUS)
priority_dict = dict(CHOICES_PRIORITY)


# Inserts stats
@tasks.context_processor
def inject():
    return inject_user_sidebar_stats()


# LIST
@tasks.route("/", methods=('GET', 'POST'))
@login_required
def index():
    form_search = FormTasksSearch
    users = get_users()
    if 'search' in request.args:
        tasks = search_tasks(json.dumps(request.args))
        return render_template('tasks/index.html',
                               tasks=tasks,
                               users=users,
                               form_search=form_search,
                               status_dict=status_dict,
                               priority_dict=priority_dict,
                               )
    elif 'filter' in request.args:
        tasks = get_tasks(request.args.get('status', ''))
    else:
        tasks = get_tasks('6', 'not')
    return render_template('tasks/index.html',
                           tasks=tasks,
                           users=users,
                           form_search=form_search,
                           status_dict=status_dict,
                           priority_dict=priority_dict
                           )


# VIEW
@tasks.route("/<task_id>", methods=['GET'])
@login_required
def view(task_id):
    form_task = FormTask()
    form_comment = FormComment()
    users = get_users()
    contacts = get_contacts()
    comments = get_comments('task', task_id)
    task = get_task(task_id)
    return render_template('tasks/view.html',
                           contacts=contacts,
                           comments=comments,
                           form_task=form_task,
                           form_comment=form_comment,
                           task=task,
                           users=users,
                           status_dict=status_dict,
                           priority_dict=priority_dict
                           )


# ADD
@tasks.route("/add", methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        form_task = FormTask(request.form)
        # TODO: Form currently doesn't validate with filled-in due date
        # form_task.due.data = date_time_from_input(form_task.due.raw_data)
        # valid: "2083-01-14 18:02:00"
        if form_task.validate():
            if 'contact_id' in request.args:
                save_task(form_task, request.args.get('contact_id'))
            else:
                save_task(form_task, None)
                flash(gettext('A new task has been added.'))
            # return to origin after task has been added
            if 'return_url' in request.args:
                return redirect(request.args.get('return_url'))
            else:
                return redirect('/account/tasks')
        else:
            if form_task.errors:
                flash(form_task.errors)
    else:
        form_task = FormTask()
        # pass contact_id and return_url to form
        if 'contact_id' in request.args:
            contact = get_contact(request.args.get('contact_id'))
            flash(gettext(
                "This Task will be related to {}".format(contact.email)))
            return render_template('tasks/add.html',
                                   form_task=form_task,
                                   contact_id=contact.id,
                                   return_url=request.args.get('return_url')
                                   )
    return render_template('tasks/add.html',
                           form_task=form_task,
                           return_url=request.args.get('return_url')
                           )


# ADD ASSIGN
@tasks.route("/<task_id>/assign", methods=('GET', 'POST'))
@login_required
def assign(task_id):
    if request.method == 'POST':
        if 'user_id' in request.values:
            relate_task(task_id, 'user', request.values['user_id'])
        if 'contact_id' in request.values:
            relate_task(task_id, 'contact', request.values['contact_id'])
    return redirect('/account/tasks/{}'.format(task_id))


# EDIT
@tasks.route("/<task_id>/edit", methods=('GET', 'POST'))
@login_required
def edit(task_id):
    form = FormTask(request.form, obj=get_task(task_id))
    if form.validate_on_submit():
        update_task(form, task_id)
        if 'return_url' in request.args:
            return redirect(request.args.get('return_url'))
        else:
            return redirect('/account/tasks/{}'.format(task_id))
    else:
        if form.errors:
            flash(form.errors)
    users = get_users()
    if 'return_url' in request.args:
        return render_template('tasks/edit.html',
                               form_task=form,
                               users=users,
                               task_id=task_id,
                               return_url=request.args.get('return_url'))
    return render_template('tasks/edit.html',
                           form_task=form,
                           users=users,
                           task_id=task_id)


# COMMENT
@tasks.route("/<task_id>/comment", methods=('GET', 'POST'))
@login_required
def comment(task_id):
    form_comment = FormComment()
    if form_comment.validate_on_submit():
        result = save_comment(form_comment, task_id)
        return redirect('/account/tasks/{}#comment{}'.format(task_id, result))
    else:
        if form_comment.errors:
            flash(form_comment.errors)
    return redirect('/account/tasks/{}#comments'.format(task_id))
