"""
Set up table in database
"""
import os
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json


# DATABASE_NAME = "castingagency"
DATABASE_PATH = os.environ.get('DATABASE_URL')
if not DATABASE_PATH:
    DATABASE_NAME = "castingagency"
    DATABASE_PATH = "postgres://{}/{}".format('localhost:5432', DATABASE_NAME)
print(os.environ)
DATABASE_PATH = os.environ['DATABASE_URL']
# DATABASE_PATH = "postgres://{}/{}".format('localhost:5432', DATABASE_NAME)
db = SQLAlchemy()


def setup_db(app, database_path=DATABASE_PATH):
    """
    Initializes database
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

    # creates all tables
    db.create_all()


def db_drop_and_create_all():
    """
    Drops database then creates it
    """
    db.drop_all()
    db.create_all()


class Movie(db.Model):
    """
    Movie entity, extends the base SQLAlchemy Model
    """
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.String, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        """
        Insert record to database
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Update record to database
        """
        db.session.commit()

    def delete(self):
        """
        Remove record from database
        """
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """
        Return movie data
        """
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }


class Actor(db.Model):
    """
    Actor entity, extends the base SQLAlchemy Model
    """
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String, nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        """
        Insert record to database
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Update record to database
        """
        db.session.commit()

    def delete(self):
        """
        Remove record from database
        """
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """
        Return actor data
        """
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }
