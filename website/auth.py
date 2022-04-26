from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Вы вошли в аккаунт', category='success')
                login_user(user, remember=True)
                return redirect(url_for('routes.home'))
            else:
                flash('Неверный пароль или email, попробуйте ещё раз', category='error')
        else:
            flash('Аккаунта с таким email не существует', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Аккаунт с таким email уже существует', category='error')
        elif len(email) < 4:
            flash("Email должен быть длиннее 3-ех символов", category='error')
        elif len(firstname) < 2:
            flash("ФИО должно быть длиннее 1-го символа", category='error')
        elif password1 != password2:
            flash("Пароли не совпадают", category='error')
        elif check_password(password1) != 'ок':
            flash(check_password(password1), category='error')
        else:
            new_user = User()
            new_user.email = email
            new_user.name = firstname
            new_user.password = generate_password_hash(password1, method='sha256')
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Учётная запись создана успешно!", category='success')
            return redirect(url_for('routes.home'))

    return render_template("sign_up.html", user=current_user)


def check_password(password):
    # проверка длины пароля
    if len(password) < 8:
        return "Пароль должен включать не менее 8-ми символов"
    else:
        # проверка на подряд идущие символы и наличие цифр
        lower_password = password.lower()
        symbols_row = -1
        k_numbers = 0
        last_symbol = 0
        for symbol in list(lower_password):
            if symbols_row == -1:
                last_symbol = ord(symbol)
                symbols_row = 0
            else:
                if last_symbol + 1 == ord(symbol):
                    symbols_row += 1
                last_symbol = ord(symbol)
            if symbol.isdigit():
                k_numbers += 1
        if symbols_row > 3:
            return 'В пароле присутствуют подряд идущие символы в количестве более 3-ёх'
        else:
            if k_numbers < 1:
                return 'В пароле должна быть хоть одна цифра'
            else:
                return 'ок'
