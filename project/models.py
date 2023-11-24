from . import db
from flask_login import UserMixin


class User(UserMixin, db.Document):
    meta = {"collection": "users"}
    username = db.StringField(required=True, unique=True, max_length=50)
    email = db.EmailField(unique=True, required=True, max_length=50)
    password = db.StringField(required=True)
