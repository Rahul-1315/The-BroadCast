import flask
from application import app, db
from werkzeug.security import generate_password_hash, check_password_hash


class Admin(db.Document):
    first_name = db.StringField(max_length=20)
    last_name = db.StringField(max_length=20)
    email = db.StringField(max_length=30, unique=True)
    password = db.StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)


class User(db.Document):
    user_id = db.IntField()
    first_name = db.StringField(max_length=20)
    last_name = db.StringField(max_length=20)
    email = db.StringField(max_length=30, unique=True)
    password = db.StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)


class News(db.Document):
    news_id = db.IntField(unique=True)
    headline = db.StringField()
    author = db.StringField(max_length=30)
    description = db.StringField()
    category = db.StringField(max_length=20)
    timestamp = db.StringField(max_length=10)


class Log_file(db.Document):
    email = db.StringField()
    news_id = db.IntField()
