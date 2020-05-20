import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Actor, Movie
from .auth.auth import AuthError, requires_auth

#Install packages:
#pip3 install -r requirements.txt
#Run the app:
#set FLASK_APP=app.py
#set FLASK_ENV=development
#flask run


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='127.0.0.1', port=5000, debug=True)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

## ROUTES
@APP.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(jwt):

    actors = Actor.query.order_by(Actor.id).all()
    if len(actors) == 0:
       abort(404)

    try: 
      list_of_actors = []
      for actor in actors:
        list_of_actors.append({"name": actor.name, 
                               "role": actor.role,
                               "gender": actor.gender})
      return jsonify({
                'success': True,
                'actors': list_of_actors
                 }), 200
    except Exception:
            abort(422)

@APP.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(jwt):

    movies = Movie.query.order_by(Movie.id).all()
    if len(movies) == 0:
       abort(404)

    try: 
      list_of_movies = []
      for movie in movies:
        list_of_movies.append({"title": movie.title, 
                               "release_year": movie.release_year})
      return jsonify({
                'success': True,
                'movies': list_of_movies
                 }), 200
    except Exception:
            abort(422)

@APP.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def post_movies(jwt):
    body = request.get_json()

    if body == None:
      abort(422)

    try:
      title = body.get('title', None)
      release_year = body.get('release_year', None)
      movie = Movie(title=title, release_year=release_year)

      movie.insert()
      return jsonify({
            'success': True,
            'id': movie.id,
            }), 200
    except BaseException:
            abort(422)

@APP.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def post_actors(jwt):
    body = request.get_json()

    if body == None:
      abort(422)

    try:
      name = body.get('name', None)
      role = body.get('role', None)
      gender = body.get('gender', None)
      movie_id = body.get('movie_id', None)

      actor = Actor(name=name, role=role, gender=gender, movie_id=movie_id)

      actor.insert()
      return jsonify({
            'success': True,
            'id': actor.id,
            }), 200
    except BaseException:
            abort(422)

@APP.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_drink(jwt, id):
    body = request.get_json()
    actor = Actor.query.filter(Actor.id == id).one_or_none()
    if not actor:
       abort(404)

    name_update = body.get('name', None)
    role_update = body.get('role', None)
    gender_update = body.get('gender', None)

    try:
      if name_update:
        actor.name = name_update
      if role_update:
        actor.role = role_update
      if gender_update:  
        actor.gender = gender_update
 
      actor.update()

      return jsonify({
                    'success': True,
                    'id': id
                    }), 200
    except Exception:
           abort(422)

@APP.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(jwt, id):
    body = request.get_json()
    movie = Movie.query.filter(Movie.id == id).one_or_none()
    if not movie:
       abort(404)

    title_update = body.get('title', None)
    release_year_update = body.get('release_year', None)

    try:
      if title_update:
        movie.title = title_update
      if release_year_update:
        movie.release_year = release_year_update
 
      movie.update()

      return jsonify({
                    'success': True,
                    'id': id
                    }), 200
    except Exception:
           abort(422)

@APP.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(jwt, id):
    actor = Actor.query.filter(Actor.id == id).one_or_none()
    if actor is None:
        abort(404)

    try:
        actor.delete()
        
        return jsonify({
            'success': True,
            'delete': id,
        }), 200
    except:
        abort(422)

@APP.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(jwt, id):
    actor = Movie.query.filter(Movie.id == id).one_or_none()
    if actor is None:
        abort(404)

    try:
        movie.delete()
        
        return jsonify({
            'success': True,
            'delete': id,
        }), 200
    except:
        abort(422)

@APP.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

@APP.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@APP.errorhandler(AuthError)
def handle_AuthError(error):
    return jsonify({
        "success": False, 
        "error": error.status_code,
        "message": error.error,
        }), error.status_code