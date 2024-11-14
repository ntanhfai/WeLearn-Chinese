from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return "%s (%s)" % (self.username,self.email)

class Vocab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    word = db.Column(db.String(100), nullable=False)
    meaning = db.Column(db.String(255), nullable=True)
    pinyin_text = db.Column(db.String(255), nullable=True)
    difficulty = db.Column(db.Integer, default=0)

    user = db.relationship("User", backref=db.backref("vocab", lazy=True))


class Example(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chinese_text = db.Column(db.String(255), nullable=False, unique=True)
    pinyin_text = db.Column(db.String(255), nullable=True)
    meaning = db.Column(db.String(255), nullable=True)


class ExampleLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vocab_id = db.Column(db.Integer, db.ForeignKey("vocab.id", ondelete="CASCADE"), nullable=False)
    example_id = db.Column(db.Integer, db.ForeignKey("example.id", ondelete="CASCADE"), nullable=False)

    vocab = db.relationship("Vocab", backref=db.backref("example_links", lazy=True, cascade="all, delete-orphan"))
    example = db.relationship("Example", backref=db.backref("vocab_links", lazy=True, cascade="all, delete-orphan"))


