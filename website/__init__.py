from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
db_name = "database.db"


# создание самого приложения
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'yandex lyceum web project'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    db.init_app(app)

    from .routes import routes
    from .auth import auth

    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # импорт классов для бд
    from .models import User, Info

    create_database(app)

    # делаем логин менеджер
    login_manager = LoginManager()
    # если вышел из аккаунта, по умолчанию направляет на страницу логин
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# создание базы данных
# (в зависимости от того, существует уже или нет)
def create_database(app):
    if not path.exists('website/' + db_name):
        db.create_all(app=app)
