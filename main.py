from flask import Flask, redirect, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.users import User

from data.login_form import LoginForm
from data.register_form import RegistrationForm

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
        db_sess.commit()
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
        return render_template('personal_page.html', nickname=nickname,
                               login=login, matches_number=matches_number, rating=rating, current_user=current_user)


@app.route('/global_rating/<int:page_number>')
def rating(page_number=0):
    print(player_top.global_top_player[20 * page_number:20 * (page_number + 1)])
    return render_template('rating.html',
                           rating_list=player_top.global_top_player[20 * page_number:20 * (page_number + 1)],
                           page_number=page_number,
                           max_page_number=player_top.global_top_player_len // 20 +
                                           bool(player_top.global_top_player_len % 20))


def main():
    db_session.global_init("db/blog.sqlite")
    app.run()


main()

# Именно тут, а не вверху. Важен код выполняющийся внутри кода при импортировании
import scheduled.update_top as player_top
