from flask import (
    flash
)
from flask_babel import gettext
from flask_login import current_user
from flask_rq import get_queue
from app.email import send_email_from_input
from app.models import EmailOut
from app import db


def get_emails():
    result = EmailOut.query.all()
    return result


def send_email(data):
    new_email = EmailOut(
        name_sender=data.name_sender.data,
        name_recipient=data.name_recipient.data,
        email_recipient=data.email_recipient.data,
        subject=data.subject.data,
        message=data.message.data,
        author_id=current_user.id
    )
    db.session.add(new_email)
    db.session.commit()
    flash(gettext('New email saved to outbox, scheduled to be send.'))
    get_queue().enqueue(
        send_email_from_input,
        recipient=new_email.email_recipient,
        subject=new_email.subject,
        body=new_email.message
    )
    return 'success'
