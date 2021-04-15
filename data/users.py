import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    login = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    rating = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    matches_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)