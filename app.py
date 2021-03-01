print("app")

import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import setup_db, db_drop_and_create_all, Movie, Actor
from .auth import AuthError, requires_auth


print("sys", sys)
print("sys.path", sys.path)
sys.path.append('./')


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    @app.route("/")
    def handler():
        return jsonify({
            "success": True
        })


    @app.route('/movies')
    def get_movies():
        """
        Return all movies
        """
        movies = Movie.query.order_by(Movie.id).all()
        movies = [movie.type for movie in movies]
        try:
            if len(movies) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'movies': movies,
            })

        except:  # noqa
            abort(422)

    @app.route("/movies-detail")
    @requires_auth("get:movies-detail")
    def get_movies_detail(token):
        try:
            movies = [movie.long() for movie in Movie.query.all()]
            return jsonify({
                "success": True,
                "movies": movies
            })
        except Exception:
            abort(422)


    '''
    @TODO implement endpoint
        POST /movies
            it should create a new row in the movies table
            it should require the 'post:movies' permission
            it should contain the movie.long() data representation
        returns status code 200 and json {"success": True, "movies": movie}
        where movie an array containing only the newly created movie or
        appropriate status code indicating reason for failure
    '''


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(token):
        if request.data:
            try:
                new_movie_data = json.loads(request.data.decode("utf-8"))
                new_movie = Movie(title=new_movie_data["title"],
                                  release_date=json.dumps(new_movie_data["release_date"]))
                Movie.insert(new_movie)
                movie = list(map(Movie.long, Movie.query.all()))
                return jsonify({
                    "success": True,
                    "movies": movie
                })
            except BaseException:
                abort(422)


    '''
    @TODO implement endpoint
        PATCH /movies/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:movies' permission
            it should contain the movie.long() data representation
        returns status code 200 and json {"success": True, "movies": movie}
        where movie an array containing only the updated movie or
        appropriate status code indicating reason for failure
    '''


    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(token, movie_id):
        try:
            # force ignores the mimetype and always try to parse JSON
            body = request.get_json(force=True)
            title = body.get("title", None)
            release_date = body.get("release_date", None)
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            movie.title = title
            movie.release_date = json.dumps(release_date)
            movie.update()
            return jsonify({
                "success": True,
                "movies": [movie.long()]
            })
        except Exception as e:
            print(e)
            abort(422)


    '''
    @TODO implement endpoint
        DELETE /movies/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:movies' permission
        returns status code 200 and json {"success": True, "delete": id} where
        id is the id of the deleted record or appropriate status code indicating
        reason for failure
    '''


    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(token, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            movie.delete()
            return jsonify({
                "success": True,
                "delete": movie_id
            })

        except Exception as e:
            print(e)
            abort(422)


    # Error Handling
    '''
    Example error handling for unprocessable entity
    '''


    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable entity"
        }), 422


    '''
    @TODO implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
                 jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404
    
    '''


    '''
    @TODO implement error handler for 404
        error handler should conform to general task above
    '''


    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404


    '''
    @TODO implement error handler for AuthError
        error handler should conform to general task above
    '''


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