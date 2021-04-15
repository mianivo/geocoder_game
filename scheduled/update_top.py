import schedule
from data.users import User
from data import db_session

global_top_player = []
global_top_player_len = 0


def update_top():
    global global_top_player, global_top_player_len
    db_sess = db_session.create_session()
    users = db_sess.query(User)
    rating_list = [(user.nickname, str(user.rating), str(user.matches_number), user.login, user.id) for user in users]
    rating_list.sort(key=lambda x: (-int(x[1]), int(x[2])))
    global_top_player = rating_list
    global_top_player_len = len(global_top_player)


update_top()
schedule.every().hour.do(update_top)
