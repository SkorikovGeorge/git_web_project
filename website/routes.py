from flask import Blueprint

routes = Blueprint('routes', __name__)


@routes.route('/')
def home():
    return '<h1>Home<h1>'
