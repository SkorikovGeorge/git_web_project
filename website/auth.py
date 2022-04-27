from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


# начальная страница логина
@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # забираем введённый email и пароль
        email = request.form.get('email')
        password = request.form.get('password')

        # ищем пользователя в бд по email
        user = User.query.filter_by(email=email).first()
        if user:
            # проверка хэш пароля по бд
            if check_password_hash(user.password, password):
                flash('Вы вошли в аккаунт', category='success')
                # запомнить, что пользователь авторизовался
                login_user(user, remember=True)
                # переход на страницу личного кабинета с заметками
                return redirect(url_for('routes.home'))
            else:
                flash('Неверный пароль или email, попробуйте ещё раз', category='error')
        else:
            flash('Аккаунта с таким email не существует', category='error')

    # подгружаем html шаблон страницы
    return render_template("login.html", user=current_user)


# кнопка для выхода из аккаунта
@auth.route('/logout')
# декоратор для ограничения действий пользователя, если он не авторизован
@login_required
def logout():
    logout_user()
    # после выхода перенаправляем на страницу для входа
    return redirect(url_for('auth.login'))


# страница регистрации
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # забираем введённые данные
        email = request.form.get('email')
        firstname = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # проверяем существование такого же email в бд
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Аккаунт с таким email уже существует', category='error')
        elif check_email(email) != 'ок':
            flash(check_email(email), category='error')
        elif check_firstname(firstname) != 'ок':
            flash(check_firstname(firstname), category='error')
        elif password1 != password2:
            flash("Пароли не совпадают", category='error')
        elif check_password(password1) != 'ок':
            flash(check_password(password1), category='error')
        else:
            # добавляем пользователя в базу данных
            new_user = User()
            new_user.email = email
            new_user.name = firstname
            # хэшируем пароль
            new_user.password = generate_password_hash(password1, method='sha256')
            db.session.add(new_user)
            db.session.commit()
            # после регистрации пользователь сразу входит в личный кабинет, запоминаем
            login_user(new_user, remember=True)
            flash("Учётная запись создана успешно!", category='success')
            # переход на страницу личного кабинета
            return redirect(url_for('routes.home'))

    # подгружаем html шаблон страницы
    return render_template("sign_up.html", user=current_user)


def check_password(password):
    # проверка длины пароля
    if len(password) < 8:
        return "Пароль должен включать не менее 8-ми символов"
    else:
        # проверка на подряд идущие символы
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
            # проверка на наличие хотя бы одной цифры
            if k_numbers < 1:
                return 'В пароле должна быть хоть одна цифра'
            else:
                return 'ок'


# проверяю почту на корректность
def check_email(eml):
    lower_email = eml.lower()
    if len(lower_email) < 5:
        return 'Email должен содержать 5-ть и более символов'
    else:
        if '@' not in lower_email:
            return 'Email должна содержать символ "@"'
        else:
            if '.com' not in lower_email and '.ru' not in lower_email:
                return 'Почта должна содержать ".com" или ".ru"'
            else:
                if lower_email[-3:] != ".ru" and lower_email[-4:] != ".com":
                    return 'В email запись ".ru" или ".com" должна находиться на конце'
                else:
                    if len(lower_email) - len(lower_email.replace('.', '')) != 1:
                        return 'Email может содержать лишь одну точку'
                    else:
                        normal_symbols = 0
                        eml_first_part = lower_email.split('@')[0]
                        for symbol in eml_first_part:
                            if symbol.isalpha():
                                normal_symbols += 1
                            elif symbol.isdigit():
                                normal_symbols += 1
                        if len(eml_first_part) != normal_symbols:
                            return 'Email должен содержать только буквы и цифры'
                        else:
                            return 'ок'


# проверка ФИО на корректность
def check_firstname(name):
    lower_name = name.lower()
    # разделяю полученные данные ФИО на имя, фамилию и отчество
    # проверяю, что они все были введены
    list_of_name_parts = lower_name.split()
    if len(list_of_name_parts) != 3:
        return 'ФИО - это имя, фамилия и отчество)))'
    else:
        # проверяю каждую часть ФИО на минимальную длину
        length_flag = True
        for name_part in list_of_name_parts:
            if len(name_part) < 2:
                length_flag = False
        if not length_flag:
            return 'Ваше имя, фамилия или отчество слишком короткое'
        else:
            # проверяю, что каждая часть ФИО состоит лишь из букв
            symbol_flag = True
            for name_part in list_of_name_parts:
                normal_symbols = 0
                for symbol in list(name_part):
                    if symbol.isalpha():
                        normal_symbols += 1
                if len(name_part) != normal_symbols:
                    symbol_flag = False
            if symbol_flag:
                return 'ок'
            else:
                return 'ФИО должно состоять только из букв'
