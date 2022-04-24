from flask import Blueprint, render_template
from flask_login import current_user


routes = Blueprint('routes', __name__)


@routes.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)