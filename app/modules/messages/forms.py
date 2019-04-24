from app.models import (
    Message
)
from app.modules import ModelForm


class FormMessage(ModelForm):
    class Meta:
        model = Message
        only = ['message',
                'conversation_id']


class FormNewConversation:
    def __init__(self, subject, message, recipient, offer):
        self.subject = subject
        self.message = message
        self.recipient = recipient
        self.offer = offer