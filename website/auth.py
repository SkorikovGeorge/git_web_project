from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return '<p>logout</p>'


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash("Email должен быть длиннее 3-ех символов", category='error')
        elif len(firstName) < 2:
            flash("ФИО должно быть длиннее 1-го символа", category='error')
        elif password1 != password2:
            flash("Пароли не совпадают", category='error')
        elif len(password1) < 7:
            flash("Пароль должен включать не менее 7-ми символов", category='error')
        else:
            # включить в базу
            flash("Учётная запись создана успешно!", category='success')

    return render_template("sign_up.html")
