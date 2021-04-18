from flask import Flask, redirect, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sqlalchemy

from data import db_session
from data.users import User
from data.games import Games
from data.login_form import LoginForm
from data.register_form import RegistrationForm
from data.delete_form import DeleteForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.is_submitted():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
def index():
    return render_template('index.html', title='Авторизация')


@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    if current_user._get_current_object().is_admin:
        form = RegistrationForm()
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()
        if not form.is_submitted():
            form.login.data = user.login
            form.nickname.data = user.nickname
            form.rating.data = user.rating
            form.matches_number.data = user.matches_number
        else:
            user.login = form.login.data
            user.nickname = form.nickname.data
            user.rating = form.rating.data
            user.matches_number = form.matches_number.data
            if form.password.data:
                user.set_password(form.password.data)
            db_sess.commit()
            player_top.update_top()
            return redirect('/admin/0')
        return render_template('edit.html', title='Авторизация', form=form)
    else:
        return 'Вы не администратор!'


@app.route('/delete/<int:user_id>', methods=['GET', 'POST'])
def delete(user_id):
    if current_user._get_current_object().is_admin:
        form = DeleteForm()
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()
        if form.is_submitted() and str(form.confirm.data) == form.confirm.label.text:
            db_sess.delete(user)
            db_sess.commit()
            player_top.update_top()
            return redirect('/admin/0')
        return render_template('delete.html', title='Авторизация', user=user, form=form)
    else:
        return 'Вы не администратор!'


@app.route('/admin')
def admin_():
    return redirect('/admin/0')


@app.route('/admin/<int:page_number>')
def admin(page_number=0):
    if current_user._get_current_object().is_admin:
        return render_template('admin.html',
                           rating_list=player_top.global_top_player[20 * page_number:20 * (page_number + 1)],
                           page_number=page_number,
                           max_page_number=player_top.global_top_player_len // 20 +
                                           bool(player_top.global_top_player_len % 20))
    else:
        return 'Вы не администратор!'


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.is_submitted():
        db_sess = db_session.create_session()
        user = User()
        user.nickname = form.nickname.data
        user.login = form.login.data
        user.set_password(form.password.data)

        db_sess.add(user)
        try:
            db_sess.commit()
        except sqlalchemy.exc.IntegrityError as e:
            if 'user.login' in str(e):
                form.login.errors = ('Пользователь с таким логином существует', )
            if 'user.hashed_password' in str(e):
                form.password.errors = ('Пользователь с таким паролем существует', )
            return render_template('register.html', title='Регистрация', form=form)
        return redirect('/login')

    return render_template('register.html', title='Авторизация', form=form)


@app.route('/not_authenticated')
def not_authenticated():
    return render_template('not_authenticated.html')


@app.route('/personal_page', methods=['GET', 'POST'])
def personal_page():
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
        return render_template('personal_page.html', nickname=nickname,
                               login=login, matches_number=matches_number, rating=rating, current_user=current_user,
                               user_game_list=user_game_list)


@app.route('/global_rating')
def rating_():
    return redirect('/global_rating/0')


@app.route('/global_rating/<int:page_number>')
def rating(page_number=0):
    return render_template('rating.html',
                           rating_list=[(nickname, raitng, matches_number) for nickname, raitng, matches_number, _, _ in
                                        player_top.global_top_player[20 * page_number:20 * (page_number + 1)]],
                           page_number=page_number,
                           max_page_number=player_top.global_top_player_len // 20 +
                                           bool(player_top.global_top_player_len % 20))


def main():
    db_session.global_init("db/blog.sqlite")

    app.run()


main()

# Именно тут, а не вверху. Важен код выполняющийся внутри кода при импортировании
import scheduled.update_top as player_top
