from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import random


class DeleteForm(FlaskForm):
    '''Форма удаления'''
    # случайное число для удаленияэ Число меняется только при перезапуске
    # сервера, но это не важно. Это могло бы быть и конкретное число.
    confirm = StringField(str(random.randint(1, 14999)), validators=[DataRequired()])
    submit = SubmitField('Удалить')
