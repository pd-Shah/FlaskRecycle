from flask_babel import lazy_gettext
from wtforms.fields import (
    StringField,
)
from wtforms.validators import DataRequired, Length
from app.modules import ModelForm


class FormSearch(ModelForm):
    title = StringField(lazy_gettext('Search course'), validators=[DataRequired(), Length(max=60)])
