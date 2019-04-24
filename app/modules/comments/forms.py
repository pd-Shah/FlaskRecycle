from app.models import Comment
from app.modules import ModelForm


class FormComment(ModelForm):
    class Meta:
        model = Comment
        only = ['comment']
