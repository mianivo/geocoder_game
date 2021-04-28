import sqlalchemy

from .db_session import SqlAlchemyBase


class PanoramaPoints(SqlAlchemyBase):
    __tablename__ = 'panorama_points'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    y = sqlalchemy.Column(sqlalchemy.Integer)
    x = sqlalchemy.Column(sqlalchemy.Integer)
