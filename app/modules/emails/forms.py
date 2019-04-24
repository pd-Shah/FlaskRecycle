from app.models import EmailOut
from app.modules import ModelForm


class FormEmailOut(ModelForm):
    class Meta:
        model = EmailOut
        only = ['name_sender',
                'name_recipient',
                'email_recipient',
                'subject',
                'message']
