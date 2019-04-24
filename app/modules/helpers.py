from flask import (
    Blueprint
)

import pytz
import dateparser
from app.models import User

from app import db

modules = Blueprint('modules', __name__,)


def date_time_from_input(v):
    if v is not None:
        # tz = pytz.timezone('utc')
        # dt = tz.localize(dateparser.parse(str(v)))
        dt = dateparser.parse(str(v))
    else:
        dt = None
    return dt


def users_for_selection():
    u = db.session.query(User).all()
    return [(i.id, i.first_name) for i in u]
