import uuid
from flask_babel import gettext
from flask_login import current_user

from app import db
from app.models import User
from app.s3helper import s3


def get_user(_id):
    result = User.query.get(_id)
    return result


def get_users():
    result = db.session.query(User).all()
    return result


def update_account(data):
    user = User.query.get(current_user.id)
    if user.id == current_user.id:
        user.first_name = data.first_name.data
        user.last_name = data.last_name.data
        user.company_name = data.company_name.data
        user.company_address = data.company_address.data
        user.company_country = data.company_country.data
        user.company_description = data.company_description.data
        db.session.commit()
        result = gettext('User profile has been updated')
    else:
        result = gettext('Permission denied')
    return result


def add_profile_image(filename):
    user = User.query.get(current_user.id)
    if user.id == current_user.id:
        user.profile_image = filename
        db.session.commit()
    return "{}{}".format('http://recycl-images.s3.amazonaws.com/', filename)
