from flask import (
    Blueprint
)
from flask_login import current_user
from app import cache
from app.models import Contact, Task
from app.models.offers import Offer


statistics = Blueprint('statistics', __name__,)


@cache.cached(timeout=30, key_prefix='total_tasks_user')
def total_tasks_user():
    count = Task.query.filter_by(author_id=current_user.id).count()
    return count


@cache.cached(timeout=30, key_prefix='total_contacts_user')
def total_contacts_user():
    count = Contact.query.filter_by(author_id=current_user.id).count()
    return count


@cache.cached(timeout=30, key_prefix='total_offers_user')
def total_offers_user():
    count = Offer.query.filter_by(author_id=current_user.id).count()
    return count


def inject_user_sidebar_stats():
    return dict(total_tasks_user=total_tasks_user(),
                total_contacts_user=total_contacts_user(),
                total_offers_user=total_offers_user())
