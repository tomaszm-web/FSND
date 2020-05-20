import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class Actor(db.Model):
    __tablename__ = 'actors'
    # Autoincrementing, unique primary key
    id = db.Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(120), nullable=False)
    role = Column(String(120), nullable=False)
    gender = Column(String(120), nullable=False)
    movie_id = Column(Integer, db.ForeignKey('movies.id'), nullable=False)
    
    
    # Insert function
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # Update function
    def update(self):
        db.session.commit()

    # Delete function
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # Formatting function
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'gender': self.gender,
            'movie_id': self.movie_id
        }

class Movie(db.Model):
    __tablename__ = 'movies'
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(120), nullable=False)
    release_year = Column(Integer, nullable=False)

    actors = db.relationship('Actor', backref='movies')

    # Insert function
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # Update function
    def update(self):
        db.session.commit()

    # Delete function
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # Creating a formatting function
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year
        }