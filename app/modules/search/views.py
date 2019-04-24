from flask import (
    Blueprint,
    render_template,
    request,
    json
)

from .logic import search_offers
from app.models.offers import (
    RECYCLING_CHOICE_CATEGORY,
    RECYCLING_CHOICE_CONDITION,
    RECYCLING_CHOICE_UNIT,
    RECYCLING_CHOICE_PRICING_TERMS,
    RECYCLING_CHOICE_PAYMENT,
)

from app.snippets import COUNTRIES


search = Blueprint('search', __name__,
                   template_folder='templates')

rec_category = dict(RECYCLING_CHOICE_CATEGORY)
rec_condition = dict(RECYCLING_CHOICE_CONDITION)
rec_unit = dict(RECYCLING_CHOICE_UNIT)
rec_pricing_terms = dict(RECYCLING_CHOICE_PRICING_TERMS)
rec_payment = dict(RECYCLING_CHOICE_PAYMENT)
countries = dict(COUNTRIES)


# VIEW
@search.route('/search/', methods=['GET', 'POST'])
def results():
    if 'category' in request.args:
        category = request.args.get('category', '')
        results = search_offers(json.dumps(request.args))
    return render_template('search/results.html',
                           category=category,
                           results=results,
                           rec_category=rec_category,
                           rec_condition=rec_condition,
                           rec_unit=rec_unit,
                           rec_pricing_terms=rec_pricing_terms,
                           rec_payment=rec_payment,
                           countries=countries)
