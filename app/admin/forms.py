from flask_babel import lazy_gettext
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
)

from app import db
from app.models import Role, User


class ChangeUserEmailForm(FlaskForm):
    email = EmailField(
        lazy_gettext('New email'), validators=[InputRequired(),
                                               Length(1, 64),
                                               Email()])
    submit = SubmitField(lazy_gettext('Update email'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(lazy_gettext('Email already registered.'))


class ChangeAccountTypeForm(FlaskForm):
    role = QuerySelectField(
        'New account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    submit = SubmitField(lazy_gettext('Update role'))


class InviteUserForm(FlaskForm):
    role = QuerySelectField(
        'Account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    first_name = StringField(
        lazy_gettext('First name'), validators=[InputRequired(),
                                                Length(1, 64)])
    last_name = StringField(
        lazy_gettext('Last name'), validators=[InputRequired(),
                                               Length(1, 64)])
    email = EmailField(
        lazy_gettext('Email'), validators=[InputRequired(),
                                           Length(1, 64),
                                           Email()])
    submit = SubmitField(lazy_gettext('Invite'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(lazy_gettext('Email already registered.'))


class NewUserForm(InviteUserForm):
    password = PasswordField(
        lazy_gettext('Password'),
        validators=[
            InputRequired(),
            EqualTo('password2', lazy_gettext('Passwords must match.'))
        ])
    password2 = PasswordField(lazy_gettext('Confirm password'),
                              validators=[InputRequired()])

    submit = SubmitField(lazy_gettext('Create'))
