from app.modules import ModelForm
from app.models.offers import Offer, OfferMatching


class FormOffer(ModelForm):
    class Meta:
        model = Offer
        only = ['summary',
                'category',
                'condition',
                'quantity',
                'unit',
                'unit_price',
                'pricing_terms',
                'place_of_delivery',
                'payment_method',
                'target_market',
                'description',
                'published']


class FormOfferMatching(ModelForm):
    class Meta:
        model = OfferMatching
        only = ['category',
                'condition',
                'target_market']
