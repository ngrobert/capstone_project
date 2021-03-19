"""
Casting agency tests
"""
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor
from app import create_app


# pylint: disable=too-many-instance-attributes, too-many-public-methods
class CastingAgencyTestCase(unittest.TestCase):
    """
    Casting agency test case
    """
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        # mock database connection
        self.database_name = "castingagency"
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                       self.database_name)
        setup_db(self.app, self.database_path)

        # auth tokens for respective roles
        self.casting_assistant = {
            "Authorization": "Bearer {}".format(os.environ.get('ASSISTANT_TOKEN'))
        }
        self.casting_director = {
            "Authorization": "Bearer {}".format(os.environ.get('DIRECTOR_TOKEN'))
        }
        self.casting_producer = {
            "Authorization": "Bearer {}".format(os.environ.get('PRODDUCER_TOKEN'))

        self.new_actor = {
            "name": "Tom Hanks",
            "age": "21",
            "gender": "Male"
        }
        self.new_movie = {
            "title": "Forest Gump",
            "release_date": "1111-22-33",
        }

        # need to use functionality that interfaces with app
        # bind app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""

    # Tests for unauthorized user
    def test_no_access_get_actors(self):
        """
        Tests only role based access control users can view actors data
        """
        response = self.client().get('/actors', headers={
            "Authorization": "Bearer UNAUTHORIZED"
        })

        self.assertEqual(response.status_code, 401)

    def test_no_access_get_movies(self):
        """
        Tests only role based access control users can view actors data
        """
        response = self.client().get('/movies', headers={
            "Authorization": "Bearer UNAUTHORIZED"
        })

        self.assertEqual(response.status_code, 401)

    # Tests for casting assistant
    def test_assistant_get_actors(self):
        """
        Tests casting assistant can view actors data
        """
        response = self.client().get('/actors',
                                     headers=self.casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_assistant_get_movies(self):
        """
        Tests casting assistant can view movies data
        """
        response = self.client().get('/movies',
                                     headers=self.casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_assistant_post_actors(self):
        """
        Tests casting assistant cannot create actor
        """
        response = self.client().post('/actors',
                                      headers=self.casting_assistant,
                                      json=self.new_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_post_movies(self):
        """
        Tests casting assistant cannot create movies
        """
        response = self.client().post('/movies',
                                      headers=self.casting_assistant,
                                      json=self.new_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_patch_actors(self):
        """
        Tests casting assistant cannot update actor
        """
        response = self.client().patch('/actors/1',
                                       headers=self.casting_assistant,
                                       json=self.new_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_patch_movies(self):
        """
        Tests casting assistant cannot update movies
        """
        response = self.client().patch('/movies/1',
                                       headers=self.casting_assistant,
                                       json=self.new_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_delete_actors(self):
        """
        Tests casting assistant cannot delete actor
        """
        response = self.client().delete('/actors/1',
                                        headers=self.casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_delete_movies(self):
        """
        Tests casting assistant cannot delete movies
        """
        response = self.client().delete('/movies/1',
                                        headers=self.casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Tests for casting director
    def test_director_get_actors(self):
        """
        Tests casting director can view actors data
        """
        response = self.client().get('/actors',
                                     headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_director_get_movies(self):
        """
        Tests casting director can view movies data
        """
        response = self.client().get('/movies',
                                     headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_director_post_actors(self):
        """
        Tests casting director can create actor
        """
        total_actors_before = len(Actor.query.all())
        response = self.client().post('/actors',
                                      headers=self.casting_director,
                                      json=self.new_actor)
        data = json.loads(response.data)
        total_actors_after = total_actors_before + 1

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(total_actors_after, 1)

    def test_director_post_movies(self):
        """
        Tests casting director can create movies
        """
        response = self.client().post('/movies',
                                      headers=self.casting_director,
                                      json=self.new_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_director_patch_actors(self):
        """
        Tests casting director can update actor
        """
        before_update = self.client().get('/actors',
                                          headers=self.casting_director)
        before_update = json.loads(before_update.data)["actors"][0]
        update_actor = {'name': before_update["name"] + "S"}
        response = self.client().patch('/actors/24',
                                       headers=self.casting_director,
                                       json=update_actor)
        data = json.loads(response.data)
        after_update = data["actors"][0]

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(before_update, after_update, "Update successful")

    def test_director_patch_movies(self):
        """
        Tests casting director can update movies
        """
        before_update = self.client().get('/movies',
                                          headers=self.casting_director)
        before_update = json.loads(before_update.data)["movies"][0]
        update_movie = {'title': before_update["title"] + "S"}
        response = self.client().patch('/movies/10',
                                       headers=self.casting_director,
                                       json=update_movie)
        data = json.loads(response.data)
        after_update = data

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(before_update, after_update, "Update successful")

    def test_director_delete_actors(self):
        """
        Tests casting director can delete actor
        """
        response = self.client().delete('/actors/26',
                                        headers=self.casting_director)
        data = json.loads(response.data)
        actor = Actor.query.filter(Actor.id == 26).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 26)
        self.assertEqual(actor, None)

    def test_director_delete_movies(self):
        """
        Tests casting director cannot delete movies
        """
        response = self.client().delete('/movies/1',
                                        headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Tests for casting producer
    def test_producer_get_actors(self):
        """
        Tests casting producer can view actors data
        """
        response = self.client().get('/actors',
                                     headers=self.casting_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_producer_get_movies(self):
        """
        Tests casting producer can view movies data
        """
        response = self.client().get('/movies',
                                     headers=self.casting_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_producer_post_actors(self):
        """
        Tests casting producer can create actor
        """
        total_actors_before = len(Actor.query.all())
        response = self.client().post('/actors',
                                      headers=self.casting_producer,
                                      json=self.new_actor)
        data = json.loads(response.data)
        total_actors_after = total_actors_before + 1

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(total_actors_after, 1)

    def test_producer_post_movies(self):
        """
        Tests casting producer can create movies
        """
        total_movies_before = len(Movie.query.all())
        response = self.client().post('/movies', headers=self.casting_producer,
                                      json=self.new_movie)
        data = json.loads(response.data)
        total_movies_after = total_movies_before + 1

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(total_movies_after, 1)

    def test_producer_patch_actors(self):
        """
        Tests casting producer can update actor
        """
        before_update = self.client().get('/actors',
                                          headers=self.casting_producer)
        before_update = json.loads(before_update.data)["actors"][0]
        update_actor = {'name': before_update["name"] + "S"}
        response = self.client().patch('/actors/24',
                                       headers=self.casting_producer,
                                       json=update_actor)
        data = json.loads(response.data)
        after_update = data["actors"][0]

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(before_update, after_update, "Update successful")

    def test_producer_patch_movies(self):
        """
        Tests casting producer can update movies
        """
        before_update = self.client().get('/movies',
                                          headers=self.casting_producer)
        before_update = json.loads(before_update.data)["movies"][0]
        update_movie = {'title': before_update["title"] + "S"}
        response = self.client().patch('/movies/10',
                                       headers=self.casting_producer,
                                       json=update_movie)
        data = json.loads(response.data)
        after_update = data

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(before_update, after_update, "Update successful")

    def test_producer_delete_actors(self):
        """
        Tests casting producer can delete actor
        """
        response = self.client().delete('/actors/27',
                                        headers=self.casting_producer)
        data = json.loads(response.data)
        actor = Actor.query.filter(Actor.id == 27).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 27)
        self.assertEqual(actor, None)

    def test_producer_delete_movies(self):
        """
        Tests casting producer cannot delete movies
        """
        response = self.client().delete('/movies/19',
                                        headers=self.casting_producer)
        data = json.loads(response.data)
        movie = Movie.query.filter(Movie.id == 19).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 19)
        self.assertEqual(movie, None)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
