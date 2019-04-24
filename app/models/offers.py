from flask_babel import lazy_gettext
from wtforms.widgets import TextArea, RadioInput
from sqlalchemy_utils import ChoiceType

from app import db
from app.models._mixin import TimestampMixin, AuthorMixin
from app.models.user import User
from app.snippets import COUNTRIES

RECYCLING_CHOICE_CATEGORY = [(u'', lazy_gettext('Select Category')),
                             (u'1', lazy_gettext('other')),
                             (u'2', lazy_gettext('ABS')),
                             (u'3', lazy_gettext('Acrylic')),
                             (u'4', lazy_gettext('EPS')),
                             (u'5', lazy_gettext('EVA')),
                             (u'6', lazy_gettext('HDPE')),
                             (u'7', lazy_gettext('HIPS')),
                             (u'8', lazy_gettext('LDPE')),
                             (u'9', lazy_gettext('LLDPE')),
                             (u'10', lazy_gettext('Nylon')),
                             (u'11', lazy_gettext('PA')),
                             (u'12', lazy_gettext('PC')),
                             (u'13', lazy_gettext('PET PETE')),
                             (u'14', lazy_gettext('PP')),
                             (u'15', lazy_gettext('PPRC')),
                             (u'16', lazy_gettext('PS')),
                             (u'17', lazy_gettext('PVC')),
                             (u'18', lazy_gettext('Tires'))]

RECYCLING_CHOICE_CONDITION = [(u'', lazy_gettext('Select Condition')),
                              (u'1', lazy_gettext('other')),
                              (u'2', lazy_gettext('Baled')),
                              (u'3', lazy_gettext('Clean flake')),
                              (u'4', lazy_gettext('Colored')),
                              (u'5', lazy_gettext('Densified')),
                              (u'6', lazy_gettext('Fiber')),
                              (u'7', lazy_gettext('Loose')),
                              (u'8', lazy_gettext('Lump')),
                              (u'9', lazy_gettext('Mixed')),
                              (u'10', lazy_gettext('Off spec')),
                              (u'11', lazy_gettext('Pellet')),
                              (u'12', lazy_gettext('Regrind')),
                              (u'13', lazy_gettext('Rolls')),
                              (u'14', lazy_gettext('Virgin')),
                              (u'15', lazy_gettext('Prime')),
                              (u'16', lazy_gettext('Masterbatch')),
                              (u'17', lazy_gettext('Compound'))]


RECYCLING_CHOICE_UNIT = [(u'', lazy_gettext('Select Unit')),
                         (u'1', lazy_gettext('Lbs')),
                         (u'2', lazy_gettext('MT')),
                         (u'3', lazy_gettext('Kg'))]


RECYCLING_CHOICE_PRICING_TERMS = [(u'', lazy_gettext('Select Terms')),
                                  (u'1', lazy_gettext('other')),
                                  (u'2', lazy_gettext('EXW')),
                                  (u'3', lazy_gettext('FCA')),
                                  (u'4', lazy_gettext('FAS')),
                                  (u'5', lazy_gettext('FOB')),
                                  (u'6', lazy_gettext('CFR')),
                                  (u'7', lazy_gettext('CIF')),
                                  (u'8', lazy_gettext('DAF')),
                                  (u'9', lazy_gettext('DES')),
                                  (u'10', lazy_gettext('DEQ')),
                                  (u'11', lazy_gettext('DDU'))]


RECYCLING_CHOICE_PAYMENT = [(u'', lazy_gettext('Select Payment Method')),
                            (u'1', lazy_gettext('Other')),
                            (u'2', lazy_gettext('L/C')),
                            (u'3', lazy_gettext('Cash'))]


class OfferImage(TimestampMixin, AuthorMixin, db.Model):
    __tablename__ = 'offers_images'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(
        db.String(100),
        nullable=False)
    offer_id = db.Column(
        db.Integer,
        db.ForeignKey('offers.id'),
        nullable=False)


class Offer(TimestampMixin, AuthorMixin, db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(
        db.String(100),
        info={'label': lazy_gettext('What are you selling?')})
    category = db.Column(
        ChoiceType(RECYCLING_CHOICE_CATEGORY),
        info={'label': lazy_gettext('Category')},
        nullable=False)
    condition = db.Column(
        ChoiceType(RECYCLING_CHOICE_CONDITION),
        info={'label': lazy_gettext('Condition')},
        nullable=False)
    quantity = db.Column(
        db.String(100),
        info={'label': lazy_gettext('Quantity')})
    unit = db.Column(
        ChoiceType(RECYCLING_CHOICE_UNIT),
        info={'label': lazy_gettext('Unit')},
        nullable=False)
    unit_price = db.Column(
        db.String(100),
        info={'label': lazy_gettext('Price per Unit')})
    pricing_terms = db.Column(
        ChoiceType(RECYCLING_CHOICE_PRICING_TERMS),
        info={'label': lazy_gettext('Pricing Terms')},
        nullable=False)
    place_of_delivery = db.Column(
        db.String(100),
        info={'label': lazy_gettext('Location')})
    payment_method = db.Column(
        ChoiceType(RECYCLING_CHOICE_PAYMENT),
        info={'label': lazy_gettext('Payment')},
        nullable=False)
    target_market = db.Column(
        ChoiceType(COUNTRIES),
        info={'label': lazy_gettext('Target Market')},
        nullable=False)
    description = db.Column(
        db.String(100),
        info={'label': lazy_gettext('Description'),
              'widget': TextArea()})
    published = db.Column(
        db.Boolean(),
        info={'label': lazy_gettext('Published'),
              'widget': RadioInput()})
    images = db.relationship('OfferImage', backref='offer', lazy=True)


    @staticmethod
    def generate_fake(count=100, **kwargs):
        """Generate a number of fake offers for testing."""
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker
        from random import randint
        import lorem

        fake = Faker()
        users = User.query.all()

        seed()
        for i in range(count):
            u = Offer(
                summary=lorem.sentence(),
                category=randint(1, 18),
                condition=randint(1, 17),
                quantity=randint(0, 100),
                unit=randint(1, 3),
                # unit=choice(RECYCLING_CHOICE_UNIT)[0],
                unit_price=randint(0, 1000),
                pricing_terms=randint(1, 11),
                place_of_delivery=fake.address(),
                payment_method=randint(1, 3),
                target_market=choice(COUNTRIES)[0],
                description=lorem.sentence(),
                published=True,
                author_id=randint(1, 20),
                created=fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=1),
                **kwargs)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class OfferMatching(TimestampMixin, AuthorMixin, db.Model):
    __tablename__ = 'offers_matchings'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(
        ChoiceType(RECYCLING_CHOICE_CATEGORY),
        info={'label': lazy_gettext('Category')},
        nullable=False)
    condition = db.Column(
        ChoiceType(RECYCLING_CHOICE_CONDITION),
        info={'label': lazy_gettext('Condition')},
        nullable=False)
    target_market = db.Column(
        ChoiceType(COUNTRIES),
        info={'label': lazy_gettext('Target Market')},
        nullable=False)
