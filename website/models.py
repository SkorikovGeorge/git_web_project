from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(100))
    all_info = db.relationship('Info')


class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(20000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))