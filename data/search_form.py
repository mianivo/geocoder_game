from wtforms import StringField, SubmitField, IntegerField
from flask_wtf import FlaskForm


class SearchForm(FlaskForm):
    nickname = StringField('Ник')
    login = StringField('Логин')
    rating = IntegerField('Рейтинг')
    matches_number = IntegerField('Количество матчей')
    submit = SubmitField('Поиск')
