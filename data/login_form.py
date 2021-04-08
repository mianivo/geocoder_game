from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    rating = IntegerField('Рейтинг', validators=[DataRequired()], default=0)
    matches_number = IntegerField('Рейтинг', validators=[DataRequired()], default=0)
    submit = SubmitField('Войти')