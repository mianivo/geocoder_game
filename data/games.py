import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Games(SqlAlchemyBase, UserMixin):
    __tablename__ = 'game'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    start_point = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_input_point = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    rating = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("user.id"))
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user = orm.relation('User')



