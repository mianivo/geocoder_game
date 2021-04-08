from wtforms import BooleanField, StringField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    nickname = StringField('Ник')
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Введите уникальный пароль', [validators.DataRequired(),
        validators.EqualTo('repeat_password', message='Пароли должны совпадать')])
    repeat_password = PasswordField('Repeat Password')
    submit = SubmitField('Войти')
