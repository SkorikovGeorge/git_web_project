from flask_login import UserMixin
from . import db


# класс для таблицы с данными о пользователе
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(100))
    # внешний ключ
    all_info = db.relationship('Info')


# класс для таблицы с заметками пользователей
class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(20000))
    # внешний ключ - id пользователя
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
