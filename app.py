"""
Casting agency app
"""
import sys
from flask import Flask, request, abort, jsonify
from models import setup_db, db_drop_and_create_all, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
    """
    create and configure the app
    """
    app = Flask(__name__)
    setup_db(app)

    @app.route("/")
    def handler():
        return jsonify({
            "success": True
        })

    """
    Movies Endpoints
    """
    @app.route('/movies')
    @requires_auth('get:movies')
    # @requires_auth decorator passes token argument when calling respective
    # method
    def get_movies(token):
        """
        Return all movies
        """
        all_movies = Movie.query.all()
        movies = [movie.format() for movie in all_movies]

        try:
            if len(movies) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'movies': movies,
            })

        except:
            abort(422)


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(token):
        """
        Adds new movie to the database
        """
        if request.data:
            try:
                # parse data as json
                new_movie_data = request.get_json('movie')
                title = new_movie_data["title"]
                release_date = new_movie_data["release_date"]
                movie_db = Movie(title, release_date)
                movie_db.insert()
                movie = [movie_db.format()]

                return jsonify({
                    "success": True,
                    "movies": movie
                })

            except BaseException:
                abort(422)


    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(token, movie_id):
        """
        Update movie information
        """
        try:
            body = request.get_json(force=True)
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            title = body["title"] if "title" in body else movie.title
            release_date = body["release_date"] if "release_date" in body else movie.release_date
            movie.title = title
            movie.release_date = release_date
            movie.update()

            return jsonify({
                "success": True,
                "movies": [movie.format()]
            })

        except Exception as e:
            print(e)
            abort(422)


    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(token, movie_id):
        """
        Remove movie from database
        """
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            movie.delete()

            return jsonify({
                'success': True,
                'delete': movie_id
            })

        except Exception as e:
            print(sys.exc_info())
            abort(422)


    """
    Actors Endpoints
    """
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(token):
        """
        Return all actors
        """
        all_actors = Actor.query.all()
        actors = [actor.format() for actor in all_actors]
        print("actors", actors)

        try:
            if len(actors) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'actors': actors,
            })

        except:  # noqa
            abort(422)


    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(token):
        """
        Adds new actor to the database
        """
        if request.data:
            try:
                # parse data as json
                new_actor_data = request.get_json('actor')
                name = new_actor_data["name"]
                age = new_actor_data["age"]
                gender = new_actor_data["gender"]

                actor_db = Actor(name, age, gender)
                actor_db.insert()
                actor = [actor_db.format()]

                return jsonify({
                    "success": True,
                    "actors": actor
                })

            except BaseException:
                abort(422)


    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(token, actor_id):
        """
        Update actor information
        """
        try:
            body = request.get_json(force=True)
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            name = body["name"] if "name" in body else actor.name
            age = body["age"] if "age" in body else actor.age
            gender = body["gender"] if "gender" in body else actor.gender
            actor.name = name
            actor.age = age
            actor.gender = gender
            actor.update()

            return jsonify({
                "success": True,
                "actors": [actor.format()]
            })

        except Exception as e:
            print(e)
            abort(422)


    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(token, actor_id):
        """
        Remove actor from database
        """
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            actor.delete()

            return jsonify({
                'success': True,
                'delete': actor_id
            })

        except Exception as e:
            print(sys.exc_info())
            abort(422)


    # Error Handling
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable entity"
        }), 422


    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        """
        Handle global auth errors
        """
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
