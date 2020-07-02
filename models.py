"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def _get_date():
    return datetime.datetime.now()

def connect_db(app):
    """Connect to db"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ Model for each user in db """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(1000), nullable=True,
    default="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1200px-No_image_available.svg.png")
    user_posts= db.relationship('Post',backref='users',cascade="all, delete-orphan")
    @property
    def get_full_name(self):
        """ return user full name """
        return f'{self.first_name} {self.last_name}'


class Post(db.Model):
    """ Model for each post """
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.String(3000),nullable=False)
    created_at = db.Column(db.Date(),nullable=True, default=_get_date())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='posts', foreign_keys=[user_id]) 
