from flask import Blueprint, render_template
from flask_login import current_user, login_required

routes = Blueprint('routes', __name__)


@routes.route('/')
def home():
    return render_template("home.html", user=current_user)