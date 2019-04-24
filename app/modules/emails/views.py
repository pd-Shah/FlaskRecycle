from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    flash,
)
from flask_babel import gettext
from flask_login import login_required

from app.models import EmailOut
from .forms import *
from .logic import get_emails, send_email

from app.modules.contacts.logic import get_contact


emails = Blueprint('emails', __name__,
                   template_folder='templates')


# List
@emails.route("/")
@login_required
def index():
    emails_out = get_emails()
    return render_template('emails/index.html',
                           emails=emails_out
                           )


# View
@emails.route("/<email_id>/")
@login_required
def view(email_id):
    email = EmailOut.query.get(email_id)
    return render_template('emails/view.html',
                           email=email
                           )


# ADD
@emails.route("/send", methods=('GET', 'POST'))
@login_required
def send():
    form_email = FormEmailOut()
    if form_email.validate_on_submit():
        send_email(form_email)
        if 'return_url' in request.args:
            return redirect(request.args.get('return_url'))
        return redirect('/account/emails/')
    if 'contact_id' in request.args and 'return_url' in request.args:
        contact = get_contact(request.args.get('contact_id'))
        form_email.email_recipient.data = contact.email
        flash(gettext(
            'Sending email to {}'.format(contact.email)
        ))
        return_url = request.args.get('return_url')
        return render_template('emails/send.html',
                               form_email=form_email,
                               contact=contact,
                               return_url=return_url
                               )
    return render_template('emails/send.html',
                           form_email=form_email
                           )
