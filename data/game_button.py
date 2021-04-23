from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
import wtforms


class ConfirmPlace(FlaskForm):
    rating = StringField(validators=[DataRequired()])
    submit = SubmitField('Подтвердить')