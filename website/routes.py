from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Info
from ast import literal_eval


routes = Blueprint('routes', __name__)


@routes.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        user_text = request.form.get('info')
        find_text = request.form.get('find')
        if find_text:
            all_user_info = Info.query.filter_by(user_id=current_user.id).all()
            result = []
            for i in all_user_info:
                if find_text in i.info:
                    result.append(i.info)
                    # result - список текстов найденных с find_text заметок
            if result:
                return redirect(url_for('routes.results', result=result))
            else:
                flash('По вашему запросу ничего не найдено', category='error')

        else:
            if len(user_text) < 1:
                flash('Текст слишком короткий, попробуйте ещё раз', category='error')
            else:
                new_text = Info(user_id=current_user.id)
                new_text.info = user_text
                db.session.add(new_text)
                db.session.commit()
                flash('Текст добавлен', category='success')

    return render_template("home.html", user=current_user)


@routes.route('/results/<result>')
def results(result):
    return render_template('results.html', result=literal_eval(result), user=current_user)


@routes.route('/delete-info/<int:id>')
def delete_info(id):
    text_to_delete = Info.query.get_or_404(id)

    try:
        db.session.delete(text_to_delete)
        db.session.commit()
        return redirect(url_for('routes.home'))
    except:
        return 'Ошибка удаления'
