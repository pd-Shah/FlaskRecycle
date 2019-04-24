from sqlalchemy import func
from flask_login import current_user

from app import db
from app.models.offers import (
    Offer,
    OfferImage,
    OfferMatching,
    RECYCLING_CHOICE_CATEGORY
)


""" ---- Offer ---------------------- """


def is_author(user_id, record):
    if record.author_id == user_id:
        return True
    else:
        return False


def get_offer(_id):
    result = Offer.query.get(_id)
    return result


def get_offers(**kwargs):
    if 'user_id' in kwargs:
        result = Offer.query.filter_by(author_id=kwargs.get('user_id'))\
                            .order_by(Offer.created).all()
    else:
        result = Offer.query.order_by(Offer.created).all()
    return result


def add_offer(data):
    new_offer = Offer(
        summary=data.summary.data,
        category=data.category.data,
        condition=data.condition.data,
        quantity=data.quantity.data,
        unit=data.unit.data,
        unit_price=data.unit_price.data,
        pricing_terms=data.pricing_terms.data,
        place_of_delivery=data.place_of_delivery.data,
        payment_method=data.payment_method.data,
        target_market=data.target_market.data,
        description=data.description.data,
        author_id=current_user.id
    )
    db.session.add(new_offer)
    db.session.commit()
    return 'Offer has been published', new_offer.id


def add_offer_image(filename, offer_id):
    offer = Offer.query.get(offer_id)
    if is_author(current_user.id, offer):
        new_image = OfferImage(
            image=filename,
            offer_id=offer.id,
            author_id=current_user.id
        )
        db.session.add(new_image)
        db.session.commit()
    return 'ok'


def replace_offer_image(filename, offer_id):
    offer = Offer.query.get(offer_id)
    if is_author(current_user.id, offer):
        for image in offer.images:
            db.session.delete(image)
        new_image = OfferImage(
            image=filename,
            offer_id=offer.id,
            author_id=current_user.id
        )
        db.session.add(new_image)
        db.session.commit()
    return 'ok'


def update_offer(data, _id):
    offer = Offer.query.get(_id)
    if is_author(current_user.id, offer):
        offer.summary=data.summary.data,
        offer.category=data.category.data,
        offer.condition=data.condition.data,
        offer.quantity=data.quantity.data,
        offer.unit=data.unit.data,
        offer.unit_price=data.unit_price.data,
        offer.pricing_terms=data.pricing_terms.data,
        offer.place_of_delivery=data.place_of_delivery.data,
        offer.payment_method=data.payment_method.data,
        offer.target_market=data.target_market.data,
        offer.description=data.description.data,
        db.session.commit()
        result = 'Offer has been updated'
    else:
        result = 'Permission denied'
    return result


def change_offer_status(_id, data):
    offer = Offer.query.get(_id)
    if is_author(current_user.id, offer):
        offer.published = data
        db.session.commit()
        if data:
            result = 'Your offer has been published'
        else:
            result = 'Your offer has been made private'
        return result


def delete_offer(offer_id):
    offer = Offer.query.get(offer_id)
    if is_author(current_user.id, offer):
        db.session.delete(offer)
        db.session.commit()
    return 'success'


def count_categories():
    result = []
    for category in RECYCLING_CHOICE_CATEGORY:
        if category[0] != '':
            count = db.session.query(func.count(Offer.id)).filter_by(category=category[0]).all()
            result.append((category[0], category[1], count[0][0]))
    return result


""" ---- OfferMatching ---------------------- """


def get_offer_matching(_id):
    result = OfferMatching.query.get(_id)
    return result


def get_offers_matchings(**kwargs):
    if 'user_id' in kwargs:
        result = OfferMatching.query.filter_by(author_id=kwargs.get('user_id'))\
                                    .order_by(OfferMatching.created).all()
    else:
        result = OfferMatching.query.order_by(OfferMatching.created).all()
    return result


def add_offer_matching(data):
    new_offer = OfferMatching(
        category=data.category.data,
        condition=data.condition.data,
        target_market=data.target_market.data,
        author_id=current_user.id
    )
    db.session.add(new_offer)
    db.session.commit()
    return 'Offer matching has been activated', new_offer.id
