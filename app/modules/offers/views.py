from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request
)
from flask_login import login_required, current_user
from app.account import get_user
from app.models.offers import (
    RECYCLING_CHOICE_CATEGORY,
    RECYCLING_CHOICE_CONDITION,
    RECYCLING_CHOICE_UNIT,
    RECYCLING_CHOICE_PRICING_TERMS,
    RECYCLING_CHOICE_PAYMENT,
)
from app.snippets import COUNTRIES

from .forms import FormOffer, FormOfferMatching
from app.modules.messages.logic import (
    create_conversation,
    get_conversations
)
from app.modules.messages.forms import FormNewConversation, FormMessage

from .logic import (
    get_offer,
    get_offers,
    add_offer,
    update_offer,
    add_offer_image,
    replace_offer_image,
    delete_offer,
    get_offer_matching,
    get_offers_matchings,
    add_offer_matching
)

from app.s3helper import check_file_before_upload, upload_file


offers = Blueprint('offers', __name__,
                                 template_folder='templates')


rec_category = dict(RECYCLING_CHOICE_CATEGORY)
rec_condition = dict(RECYCLING_CHOICE_CONDITION)
rec_unit = dict(RECYCLING_CHOICE_UNIT)
rec_pricing_terms = dict(RECYCLING_CHOICE_PRICING_TERMS)
rec_payment = dict(RECYCLING_CHOICE_PAYMENT)
countries = dict(COUNTRIES)


# Index
@offers.route("/account/recycling/offers", methods=['GET'])
@login_required
def index():
    offers = get_offers(user_id=current_user.id)
    return render_template('offers/index.html',
                           offers=offers,
                           rec_category=rec_category,
                           rec_condition=rec_condition,
                           rec_unit=rec_unit,
                           rec_pricing_terms=rec_pricing_terms,
                           rec_payment=rec_payment)


# View
@offers.route('/account/recycling/offers/<offer_id>', methods=['GET'])
@login_required
def view(offer_id):
    offer = get_offer(offer_id)
    conversations = get_conversations(offer_id=offer_id)
    return render_template('offers/view.html',
                           offer=offer,
                           countries=countries,
                           rec_category=rec_category,
                           rec_condition=rec_condition,
                           rec_unit=rec_unit,
                           rec_pricing_terms=rec_pricing_terms,
                           rec_payment=rec_payment,
                           conversations=conversations)


# ADD - GET
@offers.route("/account/recycling/offers/add", methods=['GET'])
@login_required
def add():
    form = FormOffer()
    if 'category' in request.args:
        category = request.args.get('category')
        form.category.data = category
    else:
        category = None
    return render_template(
        'offers/add.html',
        form=form,
        rec_category=rec_category,
        category=category)


# ADD - POST
@offers.route("/account/recycling/offers/add", methods=['POST'])
@login_required
def add_post():
    form = FormOffer(request.form)
    if form.validate():
        result = add_offer(form)
        if "images" in request.files:
            file = request.files["images"]
            check_file_before_upload(file)
            filename = upload_file(file, 'recycl-images')
            add_offer_image(filename, result[1])
        flash(result[0])
        return redirect('/account/recycling/offers')
    else:
        if form.errors:
            flash(form.errors)
        return render_template('offers/add.html',
                               form=form)


# EDIT
@offers.route("/account/recycling/offers/<offer_id>/edit",
                            methods=('GET', 'POST'))
@login_required
def edit(offer_id):
    form = FormOffer(request.form, obj=get_offer(offer_id))
    if request.method == 'POST':
        form = FormOffer(request.form)
        if form.validate():
            result = update_offer(form, offer_id)
            if "images" in request.files:
                file = request.files["images"]
                check_file_before_upload(file)
                filename = upload_file(file, 'recycl-images')
                replace_offer_image(filename, offer_id)
            flash(result)
            return redirect('/account/recycling/offers/{}'.format(offer_id))
        else:
            if form.errors:
                flash(form.errors)
    return render_template('offers/edit.html',
                           form=form,
                           offer_id=offer_id,
                           rec_category=rec_category,
                           rec_condition=rec_condition,
                           rec_unit=rec_unit,
                           rec_pricing_terms=rec_pricing_terms,
                           rec_payment=rec_payment)


@offers.route("/account/recycling/offers/<offer_id>/edit",
                            methods=('GET', 'POST'))
@login_required
def edit_post(offer_id):
    form = FormOffer(request.form, obj=get_offer(offer_id))
    if request.method == 'POST':
        form = FormOffer(request.form)
        if form.validate():
            result = update_offer(form, offer_id)
            flash(result)
            return redirect('/account/recycling/offers')
        else:
            if form.errors:
                flash(form.errors)
    return render_template('offers/edit.html',
                           form=form,
                           offer_id=offer_id,
                           rec_category=rec_category,
                           rec_condition=rec_condition,
                           rec_unit=rec_unit,
                           rec_pricing_terms=rec_pricing_terms,
                           rec_payment=rec_payment)


# PUBLIC
# View
@offers.route("/offers/<offer_id>", methods=['GET'])
def view_public(offer_id):
    form_message = FormMessage()
    offer = get_offer(offer_id)
    seller = get_user(offer.author_id)
    if 'new_message' in request.args:
        new_message = True
    else:
        new_message = False
    return render_template('offers/public/view.html',
                           form_message=form_message,
                           offer=offer,
                           seller=seller,
                           rec_category=rec_category,
                           rec_condition=rec_condition,
                           rec_unit=rec_unit,
                           rec_pricing_terms=rec_pricing_terms,
                           rec_payment=rec_payment,
                           countries=countries,
                           new_message=new_message)


@offers.route("/offers/<offer_id>", methods=['Post'])
def start_conversation(offer_id):
    form = FormMessage(request.form)
    if form.validate():
        offer = get_offer(offer_id)
        seller = get_user(offer.author_id)
        data = FormNewConversation(
            subject=offer.summary,
            message=form.message.data,
            recipient=seller.id,
            offer=offer_id
        )
        conversation_id = create_conversation(data)
        return redirect('/account/messages/conversation/{}'.format(conversation_id))
    else:
        if form.errors:
            flash(form.errors)


""" ---- OfferMatching ---------------------- """


# Index
@offers.route("/account/recycling/offers/matchings", methods=['GET'])
@login_required
def index_matchings():
    offers_matchings = get_offers_matchings(user_id=current_user.id)
    return render_template('offers/index_matching.html',
                           offers_matchings=offers_matchings,
                           rec_category=rec_category,
                           rec_condition=rec_condition)


# ADD - GET
@offers.route("/account/recycling/offers/matching/add", methods=['GET'])
@login_required
def add_matching():
    form = FormOfferMatching()
    return render_template(
        'offers/add_matching.html',
        form=form,
        rec_category=rec_category)


# ADD - POST
@offers.route("/account/recycling/offers/matching/add", methods=['POST'])
@login_required
def add_matching_post():
    form = FormOfferMatching(request.form)
    if form.validate():
        result = add_offer_matching(form)
        flash(result[0])
        return redirect('/account/recycling/offers/matchings')
    else:
        if form.errors:
            flash(form.errors)
        return render_template('offers/add_matching.html',
                               form=form)
