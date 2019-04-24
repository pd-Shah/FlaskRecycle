from flask_babel import lazy_gettext
from wtforms.fields import (
            StringField,
            IntegerField
        )
from wtforms.validators import Length
from app.models import Task
from app.modules import ModelForm


class FormTask(ModelForm):
    class Meta:
        model = Task
        only = ['summary',
                'description',
                'due',
                'priority',
                'status']


class FormTasksSearch(ModelForm):
    summary = StringField(lazy_gettext('Search task summary'), Length(max=60))
    category = IntegerField()
    priority = IntegerField()
    assigned = IntegerField()
