from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Info


routes = Blueprint('routes', __name__)


@routes.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        user_text = request.form.get('text')

        if len(user_text) < 1:
            flash('Текст слишком короткий, попробуйте ещё раз', category='error')
        else:
            new_text = Info(user_id=current_user.id)
            new_text.info = user_text
            db.session.add(new_text)
            db.session.commit()
            flash('Текст добавлен', category='success')

    return render_template("home.html", user=current_user)