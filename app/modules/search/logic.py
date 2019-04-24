from flask import flash, json
from sqlalchemy import and_
from app import db

from app.models.offers import Offer


def search_offers(data):
    data = json.loads(data)

    if 'search' in data.keys():
        result = {}
        if 'category' in data.keys() and 'keyword' in data.keys() and 'country' in data.keys():
            result = Offer.query.filter(and_(Offer.category == data['category'],
                                             Offer.summary.like('%' + data['keyword'] + '%'),
                                             Offer.target_market == data['country'])).all()

        elif 'category' in data.keys() and 'keyword' in data.keys():
            result = Offer.query.filter(and_(Offer.category == data['category'],
                                             Offer.summary.like('%' + data['keyword'] + '%'))).all()

        elif 'category' in data.keys() and 'country' in data.keys():
            result = Offer.query.filter(and_(Offer.category == data['category'],
                                             Offer.target_market == data['country'])).all()

        elif 'category' in data.keys():
            result = Offer.query.filter_by(category=(data['category'])).all()
        return result
    else:
        return {}
