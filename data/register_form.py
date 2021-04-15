from wtforms import BooleanField, StringField, PasswordField, validators, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    nickname = StringField('Ник')
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Введите уникальный пароль',
            [validators.EqualTo('repeat_password', message='Пароли должны совпадать')])
    rating = IntegerField('Рейтинг', validators=[DataRequired()], default=0)
    matches_number = IntegerField('Количество матчей', validators=[DataRequired()], default=0)
    repeat_password = PasswordField('Repeat Password')
    submit = SubmitField('Войти')
