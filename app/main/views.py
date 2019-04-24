from flask import (
    Blueprint,
    render_template,
    request,
    session,
)

from app.models.offers import (
    RECYCLING_CHOICE_CATEGORY,
    RECYCLING_CHOICE_CONDITION,
    RECYCLING_CHOICE_UNIT,
    RECYCLING_CHOICE_PRICING_TERMS,
    RECYCLING_CHOICE_PAYMENT,
    COUNTRIES
)

from app.account.logic import get_user
from app.modules.offers.logic import get_offers


main = Blueprint('main', __name__)


rec_category = dict(RECYCLING_CHOICE_CATEGORY)
rec_condition = dict(RECYCLING_CHOICE_CONDITION)
rec_unit = dict(RECYCLING_CHOICE_UNIT)
rec_pricing_terms = dict(RECYCLING_CHOICE_PRICING_TERMS)
rec_payment = dict(RECYCLING_CHOICE_PAYMENT)
countries = dict(COUNTRIES)

from app.modules.offers.logic import count_categories


@main.route('/')
def index():
    categories_with_count = count_categories()
    return render_template('main/index.html',
                           rec_category=rec_category,
                           rec_condition=rec_condition,
                           rec_unit=rec_unit,
                           rec_pricing_terms=rec_pricing_terms,
                           rec_payment=rec_payment,
                           countries=countries,
                           categories_with_count=categories_with_count)


@main.route('/member/<user_id>', methods=["POST", "GET"])
def user_profile(user_id, current_user_id=None):
    """Get other users profile, plus follow & unfollow."""
    user = get_user(user_id)
    offers = get_offers(user_id=user_id)
    if request.method == "POST":
        login_user = get_user(session["user_id"])
        if request.form["follow"] == "unfollow":
            login_user.unfollow(user)
        else:
            login_user.follow(user)
    return render_template('main/user_profile.html',
                           user=user,
                           offers=offers,
                           rec_unit=rec_unit,
                           rec_category=rec_category,
                           rec_condition=rec_condition,
                           countries=countries,)


@main.route('/premium')
def premium():
    if 'category' in request.args:
        category = int(request.args.get('category'))
        return render_template(
            'main/premium.html',
            rec_category=rec_category,
            category=category)
    return render_template(
        'main/premium.html')


@main.route('/about')
def about():
    return render_template(
        'main/about.html')


@main.route('/contact')
def contact():
    return render_template(
        'main/contact.html')


@main.route('/tos')
def tos():
    return render_template(
        'main/tos.html')


@main.route('/impressum')
def impressum():
    return render_template(
        'main/impressum.html')


@main.route('/privacy')
def privacy():
    return render_template(
        'main/privacy.html')
