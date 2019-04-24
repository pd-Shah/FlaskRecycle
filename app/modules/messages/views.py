from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect
)
from flask_login import current_user, login_required
from app.models.offers import (
    Offer,
    RECYCLING_CHOICE_CATEGORY,
    RECYCLING_CHOICE_CONDITION,
    RECYCLING_CHOICE_UNIT,
    RECYCLING_CHOICE_PRICING_TERMS,
    RECYCLING_CHOICE_PAYMENT,
)
from app.snippets import COUNTRIES

from app.models.user import User
from .logic import get_messages, add_message, get_conversation, get_conversations, get_conversations_all
from app.modules.messages.forms import FormMessage


rec_category = dict(RECYCLING_CHOICE_CATEGORY)
rec_condition = dict(RECYCLING_CHOICE_CONDITION)
rec_unit = dict(RECYCLING_CHOICE_UNIT)
rec_pricing_terms = dict(RECYCLING_CHOICE_PRICING_TERMS)
rec_payment = dict(RECYCLING_CHOICE_PAYMENT)
countries = dict(COUNTRIES)


messages = Blueprint('messages', __name__,
                     template_folder='templates')


@messages.route("/")
@login_required
def index():
    all = get_conversations_all()
    inbox = get_conversations(recipient_id=current_user.id)
    outbox = get_conversations(user_id=current_user.id)
    return render_template('messages/index.html',
                           all=all,
                           inbox=inbox,
                           outbox=outbox)


@messages.route("/conversation/<conversation_id>", methods=('GET', 'POST'))
@login_required
def conversation(conversation_id):
    if request.method == 'POST':
        form = FormMessage(request.form)
        form.conversation_id = conversation_id
        if form.validate():
            result = add_message(form)
            flash(result)
            return redirect('/account/messages/conversation/{}'.format(conversation_id))
    else:
        form_message = FormMessage()
        conversation = get_conversation(conversation_id)
        messages = get_messages(conversation_id=conversation_id)
        if conversation._offer_id:
            offer = Offer.query.get(conversation._offer_id)
            offer_author = User.query.get(offer.author_id)
        else:
            offer = None
        return render_template('messages/conversation.html',
                               offer=offer,
                               offer_author=offer_author,
                               form_message=form_message,
                               conversation=conversation,
                               messages=messages,
                               countries=countries,
                               rec_category=rec_category,
                               rec_condition=rec_condition,
                               rec_unit=rec_unit,
                               rec_pricing_terms=rec_pricing_terms,
                               rec_payment=rec_payment)
