from flask import url_for
from flask_wtf import FlaskForm
from flask_babel import (
    lazy_gettext,
    gettext,
)
from wtforms import ValidationError
from wtforms.fields import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    SelectField,
    FileField
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from app.models import User
from app.snippets import COUNTRIES


class LoginForm(FlaskForm):
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    password = PasswordField(lazy_gettext('Password'),
                             validators=[InputRequired()])
    remember_me = BooleanField(lazy_gettext('Keep me logged in'))
    submit = SubmitField(lazy_gettext('Log in'))


class RegistrationForm(FlaskForm):
    first_name = StringField(
        lazy_gettext('First name'),
        validators=[InputRequired(),
                    Length(1, 64)])
    last_name = StringField(
        lazy_gettext('Last name'), validators=[InputRequired(),
                                               Length(1, 64)])
    email = EmailField(
        lazy_gettext('Email'), validators=[InputRequired(),
                                           Length(1, 64),
                                           Email()])
    password = PasswordField(
        lazy_gettext('Password'),
        validators=[
            InputRequired(),
            EqualTo('password2', lazy_gettext('Passwords must match'))
        ])
    password2 = PasswordField(lazy_gettext('Confirm password'),
                              validators=[InputRequired()])
    submit = SubmitField(lazy_gettext('Register'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            error_msg = '''{{ gettext('Email already registered. (Did you mean to') }}
                             <a href="{}">{{ gettext('log in') }}</a>
                             {{ gettext('instead?')}}'''.format(
                                                  url_for('account.login'))
            raise ValidationError(error_msg)


class ChangeAccountInformationForm(FlaskForm):
    first_name = StringField(
        lazy_gettext('First name'), validators=[InputRequired(),
                                                Length(1, 64)])
    last_name = StringField(
        lazy_gettext('Last name'), validators=[InputRequired(),
                                               Length(1, 64)])

    company_name = StringField(
        lazy_gettext('Name'), validators=[InputRequired(),
                                          Length(1, 64)])

    company_address = StringField(
        lazy_gettext('Address'), validators=[InputRequired(),
                                             Length(1, 256)])

    company_country = SelectField(
        lazy_gettext('Country'), choices=COUNTRIES,)

    company_description = StringField(
        lazy_gettext('Description'), validators=[InputRequired(),
                                                 Length(1, 1000)])

    submit = SubmitField(lazy_gettext('Update'))


class ChangeAccountProfilePictureForm(FlaskForm):
    profile_image = FileField(
        'Profile Image', validators=[InputRequired()])

    submit = SubmitField(lazy_gettext('Upload'))


class RequestResetPasswordForm(FlaskForm):
    email = EmailField(
        lazy_gettext('Email'), validators=[InputRequired(),
                                           Length(1, 64),
                                           Email()])
    submit = SubmitField(lazy_gettext('Reset password'))

    # We don't validate the email address so we don't confirm to attackers
    # that an account with the given email exists.


class ResetPasswordForm(FlaskForm):
    email = EmailField(
        lazy_gettext('Email'), validators=[InputRequired(),
                                           Length(1, 64),
                                           Email()])
    new_password = PasswordField(
        lazy_gettext('New password'),
        validators=[
            InputRequired(),
            EqualTo('new_password2', lazy_gettext('Passwords must match.'))
        ])
    new_password2 = PasswordField(
        lazy_gettext('Confirm new password'), validators=[InputRequired()])
    submit = SubmitField(lazy_gettext('Reset password'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(lazy_gettext('Unknown email address.'))


class CreatePasswordForm(FlaskForm):
    password = PasswordField(
        lazy_gettext('Password'),
        validators=[
            InputRequired(),
            EqualTo('password2', lazy_gettext('Passwords must match.'))
        ])
    password2 = PasswordField(
        lazy_gettext('Confirm new password'), validators=[InputRequired()])
    submit = SubmitField(lazy_gettext('Set password'))


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(lazy_gettext('Old password'),
                                 validators=[InputRequired()])
    new_password = PasswordField(
        lazy_gettext('New password'),
        validators=[
            InputRequired(),
            EqualTo('new_password2', lazy_gettext('Passwords must match.'))
        ])
    new_password2 = PasswordField(
        lazy_gettext('Confirm new password'), validators=[InputRequired()])
    submit = SubmitField(lazy_gettext('Update password'))


class ChangeEmailForm(FlaskForm):
    email = EmailField(
        lazy_gettext('New email'), validators=[InputRequired(),
                                               Length(1, 64),
                                               Email()])
    password = PasswordField(lazy_gettext('Password'), validators=[InputRequired()])
    submit = SubmitField(lazy_gettext('Update email'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(lazy_gettext('Email already registered.'))
