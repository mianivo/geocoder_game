from flask import Flask, redirect, render_template, request, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sqlalchemy

from data import db_session
from data.users import User
from data.rounds import Rounds
from data.games import Games
from data.panorama_points import PanoramaPoints
from data.login_form import LoginForm
from data.register_form import RegistrationForm
from data.delete_form import DeleteForm
from data.search_form import SearchForm
from data.game_button import ConfirmPlace
import threading
import random
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def getdistance(c1, c2):
    x = (c2[1] - c1[1])
    y = (c2[0] - c1[0])
    y *= math.cos(math.radians((c2[1] + c1[1]) / 2))
    x *= 111
    y *= 111
    return math.sqrt(x ** 2 + y ** 2)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    clear_session()
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    clear_session()
    form = LoginForm()
    if form.is_submitted():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, title='Авторизация')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
def index():
    clear_session()
    return render_template('index.html', title='Игра панорама')


@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    clear_session()
    if current_user.is_authenticated and current_user._get_current_object().is_admin:
        form = RegistrationForm()
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()
        if not form.is_submitted():
            # Если не нажата кнопка на странице редактирования
            # Автоматически заполняются поля формы
            form.login.data = user.login
            form.nickname.data = user.nickname
            form.rating.data = user.rating
            form.matches_number.data = user.matches_number
        else:
            # Если нажата запоминаем изменения
            user.login = form.login.data
            user.nickname = form.nickname.data
            user.rating = form.rating.data
            user.matches_number = form.matches_number.data
            if form.password.data:
                user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/admin/0')
        return render_template('edit.html', title='Редактирование', form=form)
    else:
        return 'Вы не администратор!'


@app.route('/delete/<int:user_id>', methods=['GET', 'POST'])
def delete(user_id):
    '''Обработчик удаления пользователей'''
    clear_session()
    if current_user.is_authenticated and current_user._get_current_object().is_admin:
        form = DeleteForm()
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()
        if not user:
            form.confirm.errors = ('Пользователь уже удален',)
        if user and form.is_submitted():
            if str(form.confirm.data) == form.confirm.label.text:
                # Проверка на совпадение числа в label и числа в поле
                db_sess.delete(user)
                db_sess.commit()
                return redirect('/admin/0')
            else:
                form.confirm.errors = ('Числа не совпадают',)
        return render_template('delete.html', title='Удаление', user=user, form=form)
    else:
        return 'Вы не администратор!'


@app.route('/admin')
def admin_():
    clear_session()
    return redirect('/admin/0')


@app.route('/admin/<int:page_number>', methods=['GET', 'POST'])
def admin(page_number=0):
    '''Админка. Имеется поиск пользователей по параметрам. Все параметры ищутся только на вхождение подстрок.
    Все найденные пользователи отображаются на 1 странице, сколько бы их не было.'''
    clear_session()
    if current_user.is_authenticated and current_user._get_current_object().is_admin:
        form = SearchForm()
        if request.method == 'POST':
            if form.login or form.nickname or form.rating or form.matches_number:
                if not form.rating.data:
                    search_rating = ''
                else:
                    search_rating = str(form.rating.data)
                if not form.matches_number.data:
                    search_matches_number = ''
                else:
                    search_matches_number = str(form.matches_number.data)
                rating_list = []
                for user in player_top.global_top_player:
                    if (form.login.data in user[3] and
                            form.nickname.data in user[0] and
                            search_rating in user[1] and
                            search_matches_number in user[2]):
                        rating_list.append(user)
            else:
                rating_list = player_top.global_top_player[20 * page_number:20 * (page_number + 1)]
        else:
            rating_list = player_top.global_top_player[20 * page_number:20 * (page_number + 1)]

        return render_template('admin.html',
                               rating_list=rating_list,
                               page_number=page_number,
                               max_page_number=player_top.global_top_player_len // 20 +
                                               bool(player_top.global_top_player_len % 20), title='админка', form=form)
    else:
        return 'Вы не администратор!'


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Регистрация'''
    clear_session()
    form = RegistrationForm()
    if form.is_submitted():
        db_sess = db_session.create_session()
        user = User()
        user.nickname = form.nickname.data
        user.login = form.login.data
        if form.password.data:
            user.set_password(form.password.data)
        else:
            form.login.errors = ('Пароль не может быть пустым',)
            return render_template('register.html', title='Регистрация', form=form)
        if form.password.data == form.repeat_password.data:
            user.set_password(form.password.data)
        else:
            form.repeat_password.errors = ('Пароли должны совпадать',)
            return render_template('register.html', title='Регистрация', form=form)

        db_sess.add(user)
        try:
            db_sess.commit()
        except sqlalchemy.exc.IntegrityError as e:
            if 'user.login' in str(e):
                form.login.errors = ('Пользователь с таким логином существует',)
            return render_template('register.html', title='Регистрация', form=form)
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/not_authenticated')
def not_authenticated():
    clear_session()
    return render_template('not_authenticated.html', title='Не авторизирован')


@app.route('/personal_page', methods=['GET', 'POST'])
def personal_page():
    '''Страница отображает ник, логин, рейтинг, кол-во матчей пользователя.
     Также отображаются последние игры пользователя.
     Если пользователь - администратор, также присутсвует кнопка войти в админку.'''
    clear_session()
    if not current_user.is_authenticated:
        return redirect('/not_authenticated')
    else:
        nickname = current_user.nickname
        login = current_user.login
        matches_number = current_user.matches_number
        rating = current_user.rating
        db_sess = db_session.create_session()
        user_game_list = db_sess.query(Games).filter(Games.user_id == current_user.id)
        if len(list(user_game_list)) > 20:
            user_game_list = user_game_list[:20]
        game_and_rounds_list = []
        for game in user_game_list:
            rounds_list = []
            for round_id in (game.round1, game.round2, game.round3, game.round4, game.round5):
                round = db_sess.query(Rounds).filter(Rounds.id == round_id).first()
                rounds_list.append(round)
            game_and_rounds_list.append((game, rounds_list))
        return render_template('personal_page.html', nickname=nickname,
                               login=login, matches_number=matches_number, rating=rating, current_user=current_user,
                               user_game_list=game_and_rounds_list, title='Личная информация')


@app.route('/global_rating')
def rating_():
    '''Отображает рейтинг, вместе с переходами по страницам.'''
    # Условия смены страниц находятся внутри шаблона
    clear_session()
    return redirect('/global_rating/0')


@app.route('/global_rating/<int:page_number>')
def rating(page_number=0):
    clear_session()
    return render_template('rating.html',
                           rating_list=[(nickname, raitng, matches_number) for nickname, raitng, matches_number, _, _ in
                                        player_top.global_top_player[20 * page_number:20 * (page_number + 1)]],
                           page_number=page_number,
                           max_page_number=player_top.global_top_player_len // 20 +
                                           bool(player_top.global_top_player_len % 20), title='Рейтинг')


@app.route('/game', methods=['GET', 'POST'])
def game():
    '''Отображает страницу с игрой и результатами раундов/игр'''
    db_sess = db_session.create_session()
    form = ConfirmPlace() # Кнопка отправки выбранных координат
    if request.method == "GET":
        # выбираются рандомные координаты из базы данных
        p = random.randint(1, db_sess.query(PanoramaPoints).count())
        p = db_sess.query(PanoramaPoints).filter(PanoramaPoints.id == p).first()
        y = p.y
        x = p.x
        y = float(y)
        x = float(x)
        y += random.randint(-100, 100) / 10000
        x += random.randint(-100, 100) / 10000
        session["x"] = x
        session["y"] = y
    if form.validate_on_submit():
        # из сессии считываются число раундов, раунды и счет
        gamenum = session.get('gamenum', 0)
        gamescore = session.get('gamescore', 0)
        rounds = session.get('rounds', [])
        x = session.get("x", 0)
        y = session.get("y", 0)
        gamenum += 1
        coords = [float(i) for i in form.rating.data.split(", ")]
        dist = getdistance([y, x], coords)
        if dist:
            score = int(5000 / (dist + 1))
            gamescore += score
            if current_user.is_authenticated:
                # если пользователь авторизирован то записываем его раунд и счет в базу данных
                curround = Rounds()
                curround.start_point = f"{x},{y}"
                curround.user_input_point = f"{coords[1]},{coords[0]}"
                curround.rating = score
                db_sess.add(curround)
                db_sess.commit()
                roundid = curround.id
                rounds.append(roundid)
                session["rounds"] = rounds
            if gamenum != 5:
                # если игра из 5 раундов все еще идет
                session["gamenum"] = gamenum
                session["gamescore"] = gamescore
                return render_template('roundresult.html', dist=dist, score=score,
                                       x1=coords[1], y1=coords[0], x2=x, y2=y,
                                       gamescore=gamescore, gamenum=gamenum)
            else:
                # если игра закончилась
                if current_user.is_authenticated:
                    # если пользователь авторизирован то записываем его игру и счет в базу данных
                    curgame = Games()
                    curgame.round1 = rounds[0]
                    curgame.round2 = rounds[1]
                    curgame.round3 = rounds[2]
                    curgame.round4 = rounds[3]
                    curgame.round5 = rounds[4]
                    curgame.rating = gamescore
                    curgame.user_id = current_user._get_current_object().id
                    db_sess.add(curgame)
                    db_sess.commit()
                clear_session()
                return render_template('gameresult.html', dist=dist, score=score,
                                       x1=coords[1], y1=coords[0], x2=x, y2=y,
                                       gamescore=gamescore, gamenum=gamenum)
    else:
        return render_template('game.html', coords=f"{y}, {x}", form=form)


def clear_session():
    '''Обнуляет число раундов, раунды и счет'''
    session["gamenum"] = 0
    session["gamescore"] = 0
    session["rounds"] = []


db_session.global_init("db/panorama_db.sqlite")

# Именно тут, а не вверху. При импортировании модуля выполняется код. Код обращается к базе данных.
import scheduled.update_top as player_top

# создается поток, чтобы обновлять список пользователей
update_top_th = threading.Thread(target=player_top.schedule_update)
update_top_th.start()
app.run()
