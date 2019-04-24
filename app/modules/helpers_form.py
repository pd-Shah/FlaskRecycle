from flask_wtf import FlaskForm

from app import db
from wtforms_alchemy import model_form_factory


BaseModelForm = model_form_factory(FlaskForm)


# https://wtforms.readthedocs.io/en/stable/fields.html
# https://wtforms-alchemy.readthedocs.io/en/latest/introduction.html#differences-with-wtforms-ext-sqlalchemy-model-form


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session
