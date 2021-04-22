from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import random


class DeleteForm(FlaskForm):
    confirm = StringField(str(random.randint(1, 14999)), validators=[DataRequired()])
    submit = SubmitField('Удалить')
