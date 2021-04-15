from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
import random


class DeleteForm(FlaskForm):
    confirm = StringField(str(random.randint(1, 9999)), validators=[DataRequired()])

    submit = SubmitField('Удалить')
