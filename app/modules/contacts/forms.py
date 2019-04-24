from app.models import Contact
from app.models import Message
from app.modules import ModelForm


class FormContact(ModelForm):
    class Meta:
        model = Contact
        only = ['first_name',
                'last_name',
                'organisation',
                'title',
                'email',
                'phone',
                'mobile',
                'description']


class FormMessage(ModelForm):
    class Meta:
        model = Message
        only = ['message']
