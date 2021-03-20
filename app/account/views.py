from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_babel import gettext
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_rq import get_queue

from app import db

from .forms import (
    ChangeEmailForm,
    ChangePasswordForm,
    CreatePasswordForm,
    LoginForm,
    RegistrationForm,
    RequestResetPasswordForm,
    ResetPasswordForm,
    ChangeAccountInformationForm,
    ChangeAccountProfilePictureForm
)
from .logic import (
    get_user,
    update_account,
    add_profile_image
)

from app.snippets import COUNTRIES
from app.email import send_email
from app.models import User
from app.s3helper import check_file_before_upload, upload_file

account = Blueprint('account', __name__)

countries = dict(COUNTRIES)


@account.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password_hash is not None and \
                user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash(gettext('You are now logged in. Welcome back!'), 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash(gettext('Invalid email or password.'), 'form-error')
    return render_template('account/logged_out/login.html', form=form)


@account.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user, and send them a confirmation email."""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        confirm_link = url_for('account.confirm', token=token, _external=True)
        get_queue().enqueue(
            send_email,
            recipient=user.email,
            subject=gettext('Confirm Your Account'),
            template='account/email/confirm',
            user=user,
            confirm_link=confirm_link)
        flash(gettext('A confirmation link has been sent to {}.'.format(
                                                                user.email)),
              'warning')
        return redirect(url_for('main.index'))
    return render_template('account/logged_out/register.html', form=form)


@account.route('/logout')
@login_required
def logout():
    logout_user()
    flash(gettext('You have been logged out.'), 'info')
    return redirect(url_for('main.index'))


@account.route('/manage', methods=['GET'])
@account.route('/manage/info', methods=['GET'])
@login_required
def manage():
    """Display a user's account information."""
    print("CURRENT USER -----------------------")
    print(current_user)
    form = ChangeAccountProfilePictureForm()
    return render_template('account/index.html', user=current_user, form=form)


@account.route('/manage', methods=['POST'])
@account.route('/manage/info', methods=['POST'])
@login_required
def upload_user_profile_image():

    if "profile_image" not in request.files:
        flash('No profile_image key in request.files')

    file = request.files["profile_image"]

    check_file_before_upload(file)
    filename = upload_file(file, 'recycl-images')
    add_profile_image(filename)

    return redirect('/account/manage/info')


@account.route('/manage/subscription', methods=['GET'])
@login_required
def manage_subscription():
    return render_template('account/subscription.html', user=current_user)


@account.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    """Respond to existing user's request to reset their password."""
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_password_reset_token()
            reset_link = url_for(
                'account.reset_password', token=token, _external=True)
            get_queue().enqueue(
                send_email,
                recipient=user.email,
                subject=gettext('Reset Your Password'),
                template='account/email/reset_password',
                user=user,
                reset_link=reset_link,
                next=request.args.get('next'))
        flash(gettext('A password reset link has been sent to {}.'.format(
                form.email.data)), 'warning')
        return redirect(url_for('account.login'))
    return render_template('account/logged_out/reset_password.html', form=form)


@account.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset an existing user's password."""
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash(gettext('Invalid email address.'), 'form-error')
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.new_password.data):
            flash(gettext('Your password has been updated.'), 'form-success')
            return redirect(url_for('account.login'))
        else:
            flash(gettext('The password reset link is invalid or has expired.'),
                  'form-error')
            return redirect(url_for('main.index'))
    return render_template('account/logged_out/reset_password.html', form=form)


@account.route('/manage/change-account-information', methods=['GET', 'POST'])
@login_required
def change_account_information():
    """Change an existing user's account information."""
    user = get_user(current_user.id)
    form = ChangeAccountInformationForm(obj=user)
    if request.method == 'POST':
        if form.validate_on_submit():
            data = form
            result = update_account(data)
            flash(result)
            return redirect(url_for('account.manage'))
        else:
            if form.errors:
                flash(form.errors)
                flash('Your input is invalid.')
    return render_template('account/change_account_information.html',
                            form=form,
                            countries=countries)


@account.route('/manage/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change an existing user's password."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash(gettext('Your password has been updated.'), 'form-success')
            return redirect(url_for('main.index'))
        else:
            flash(gettext('Original password is invalid.'), 'form-error')
    return render_template('account/change_password.html', form=form)


@account.route('/manage/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    """Respond to existing user's request to change their email."""
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            change_email_link = url_for(
                'account.change_email', token=token, _external=True)
            get_queue().enqueue(
                send_email,
                recipient=new_email,
                subject=gettext('Confirm Your New Email'),
                template='account/email/change_email',
                # current_user is a LocalProxy, we want the underlying user
                # object
                user=current_user._get_current_object(),
                change_email_link=change_email_link)
            flash(gettext('A confirmation link has been sent to {}.'.format(new_email),
                  'warning'))
            return redirect(url_for('main.index'))
        else:
            flash(gettext('Invalid email or password.'), 'form-error')
    return render_template('account/change_email.html', form=form)


@account.route('/manage/change-email/<token>', methods=['GET', 'POST'])
@login_required
def change_email(token):
    """Change existing user's email with provided token."""
    if current_user.change_email(token):
        flash(gettext('Your email address has been updated.'), 'success')
    else:
        flash(gettext('The confirmation link is invalid or has expired.'), 'error')
    return redirect(url_for('main.index'))


@account.route('/confirm-account')
@login_required
def confirm_request():
    """Respond to new user's request to confirm their account."""
    token = current_user.generate_confirmation_token()
    confirm_link = url_for('account.confirm', token=token, _external=True)
    get_queue().enqueue(
        send_email,
        recipient=current_user.email,
        subject=gettext('Confirm Your Account'),
        template='account/email/confirm',
        # current_user is a LocalProxy, we want the underlying user object
        user=current_user._get_current_object(),
        confirm_link=confirm_link)
    flash(gettext('A new confirmation link has been sent to {}.'.format(
        current_user.email)), 'warning')
    return redirect(url_for('main.index'))


@account.route('/confirm-account/<token>')
@login_required
def confirm(token):
    """Confirm new user's account with provided token."""
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm_account(token):
        flash(gettext('Your account has been confirmed.'), 'success')
    else:
        flash(gettext('The confirmation link is invalid or has expired.'),
              'error')
    return redirect(url_for('main.index'))


@account.route(
    '/join-from-invite/<int:user_id>/<token>', methods=['GET', 'POST'])
def join_from_invite(user_id, token):
    """
    Confirm new user's account with provided token and prompt them to set
    a password.
    """
    if current_user is not None and current_user.is_authenticated:
        flash(gettext('You are already logged in.'), 'error')
        return redirect(url_for('main.index'))

    new_user = User.query.get(user_id)
    if new_user is None:
        return redirect(404)

    if new_user.password_hash is not None:
        flash(gettext('You have already joined.'), 'error')
        return redirect(url_for('main.index'))

    if new_user.confirm_account(token):
        form = CreatePasswordForm()
        if form.validate_on_submit():
            new_user.password = form.password.data
            db.session.add(new_user)
            db.session.commit()
            flash(
                gettext('Your password has been set. After you log in, you can '
                        'go to the "Your Account" page to review your account '
                        'information and settings.'), 'success')
            return redirect(url_for('account.login'))
        return render_template('account/logged_out/join_invite.html', form=form)
    else:
        flash(
            gettext('The confirmation link is invalid or has expired. Another '
                    'invite email with a new link has been sent to you.'),
            'error')
        token = new_user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user_id,
            token=token,
            _external=True)
        get_queue().enqueue(
            send_email,
            recipient=new_user.email,
            subject=gettext('You Are Invited To Join'),
            template='account/email/invite',
            user=new_user,
            invite_link=invite_link)
    return redirect(url_for('main.index'))


@account.before_app_request
def before_request():
    """Force user to confirm email before accessing login-required routes."""
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:8] != 'account.' \
            and request.endpoint != 'static':
        return redirect(url_for('account.unconfirmed'))


@account.route('/unconfirmed')
def unconfirmed():
    """Catch users with unconfirmed emails."""
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('account/logged_out/unconfirmed.html')