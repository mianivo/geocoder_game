import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Games(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    round1 = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("rounds.id"))
    round2 = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("rounds.id"))
    round3 = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("rounds.id"))
    round4 = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("rounds.id"))
    round5 = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("rounds.id"))
    rating = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("user.id"))
    modifed_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user = orm.relation('User')
    roundsrel1 = orm.relation('Rounds', foreign_keys=[round1])
    roundsrel2 = orm.relation('Rounds', foreign_keys=[round2])
    roundsrel3 = orm.relation('Rounds', foreign_keys=[round3])
    roundsrel4 = orm.relation('Rounds', foreign_keys=[round4])
    roundsrel5 = orm.relation('Rounds', foreign_keys=[round5])
