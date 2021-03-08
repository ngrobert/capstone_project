import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import db, setup_db, Movie, Actor


class CastingAgencyTestCase(unittest.TestCase):
    """
    Casting agency test case
    """
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # auth tokens for respective roles
        self.casting_assistant = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1CSk5ucHk5dlNJQXpuaU1NYUF4ViJ9.eyJpc3MiOiJodHRwczovL2Rldi04ZnhjdGxlYy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA0NDMwZDAwZDlmNzEwMDcwZWU2NGM3IiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFnZW5jeS8iLCJpYXQiOjE2MTUwODE3OTQsImV4cCI6MTYxNTA4ODk5NCwiYXpwIjoiR2hyT282c3FkU2paY2txMnB1QlB2d1ZacmdrZmR5M1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.qLJxJlkos1ypQu3e755Hq1fARd-VSsQWd3zuakTx2b6hBkgBsu7b9DItigMHFF05OiXp1R2qkIUDkrBD3jQFTJoCKCRgtrXv4v2ZhkHuydwNaMmh8MWz_QxHFrWm4RlJbp_JMzqkDoumB0eBJ6yF1QTyFrA18ZFbf2NWk7HkLMIWA7YBiV2Tu9ksFGchVjFWmtB7T84L9z5_rtY9KEkHnbJw3W7eHE8ps1d2h1J4gzFY7PeA7GL0LtPTkjtvyu6bIHMUr5Tw6KKUg6XkF-rcIUglVeqVMgwktT7YNg05sXdmZIqAOKZA7EmLntjBqEj_jKne3rgr_XSYizQeF4PpaQ"
        }
        self.casting_director = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1CSk5ucHk5dlNJQXpuaU1NYUF4ViJ9.eyJpc3MiOiJodHRwczovL2Rldi04ZnhjdGxlYy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY3NzUzNWRiNDk4ZTIwMDZiOTQyNDNkIiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFnZW5jeS8iLCJpYXQiOjE2MTUwOTA1OTYsImV4cCI6MTYxNTA5Nzc5NiwiYXpwIjoiR2hyT282c3FkU2paY2txMnB1QlB2d1ZacmdrZmR5M1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.OFnRS8gpESVH3MGzvbiy8JuD2M9LebwGMplJR2FzyZJArgI6AmJhHAlGdin1P9mJRRw3-CCAsNAEcTpy_eTx_HM24ddKTAFCdlRUXiQJRE4yyZvgJVn4NR0wdXn8VvAIDGiHKJEDxKqSi83NWOnHztkIEbpBbEJcseXW9bP0SS3W1SMxxerxgEewmvb1T0nUdPgJTY5d9zd99a-ick6k65IlqMQH9wAd2Ka49CROHgizgC7VJmuYHDype8whC6yLG6eonuAhNDfVo40WbNX3HgDDumuXUeJJ3Z3daQ0PEkS0-lmL7XehpVv-tpuTFv5ZhXdF0XHriaTYftMsKGGQ6w"
        }
        self.casting_producer = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im1CSk5ucHk5dlNJQXpuaU1NYUF4ViJ9.eyJpc3MiOiJodHRwczovL2Rldi04ZnhjdGxlYy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY3NzUzOWNiYmJkODIwMDY4NjlmNDZjIiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFnZW5jeS8iLCJpYXQiOjE2MTUxNTY4MjEsImV4cCI6MTYxNTIyODgyMSwiYXpwIjoiR2hyT282c3FkU2paY2txMnB1QlB2d1ZacmdrZmR5M1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.WZcKzjRwdQ-L-_UVWdyxvlCIJ_NP0W9AA2CKFW6my4RUqY7d_IWcQCkY4LNXIuT5WobTAqTTQ0j1znQ9D98CjaDMx2aFLh0v3Ts8bZFPwviMCagxwB1-jJ69pO7CBCwkzcvYk8g5tuWm2ZwxbgdHMafqgAo_vPszM42zbg6HbjPw_I8CeNy9T7q3qMS3jKaEnscdQPDSx3iQwcnZk9xRyMuooP10P4k6XaHsXqO8oBtQs_Q2htDVK5D-s3gZSqrZXYtAw2falq88EhDtvK-IJHri35UVy-KZoIRYFISSH5CngFeHZqpP_03ZZ23IPBoI2lzTwYXdf4ogJ9SCDHqvgA"
        }

        self.new_actor = {
            "name": "Tom Hanks",
            "age": "21",
            "gender": "Male"
        }
        self.new_movie = {
            "title": "Forest Gump",
            "release_date": "1111-22-33",
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()


    def tearDown(self):
        """Executed after reach test"""
        pass


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
        response = self.client().get('/actors', headers=self.casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_assistant_get_movies(self):
        """
        Tests casting assistant can view movies data
        """
        response = self.client().get('/movies', headers=self.casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_assistant_post_actors(self):
        """
        Tests casting assistant cannot create actor
        """
        response = self.client().post('/actors', headers=self.casting_assistant, json=self.new_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_post_movies(self):
        """
        Tests casting assistant cannot create movies
        """
        response = self.client().post('/movies', headers=self.casting_assistant, json=self.new_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_patch_actors(self):
        """
        Tests casting assistant cannot update actor
        """
        response = self.client().patch('/actors/1', headers=self.casting_assistant, json=self.new_actor)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_patch_movies(self):
        """
        Tests casting assistant cannot update movies
        """
        response = self.client().patch('/movies/1', headers=self.casting_assistant, json=self.new_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_delete_actors(self):
        """
        Tests casting assistant cannot delete actor
        """
        response = self.client().delete('/actors/1', headers=self.casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_assistant_delete_movies(self):
        """
        Tests casting assistant cannot delete movies
        """
        response = self.client().delete('/movies/1', headers=self.casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Tests for casting director
    def test_director_get_actors(self):
        """
        Tests casting director can view actors data
        """
        response = self.client().get('/actors', headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_director_get_movies(self):
        """
        Tests casting director can view movies data
        """
        response = self.client().get('/movies', headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_director_post_actors(self):
        """
        Tests casting director can create actor
        """
        total_actors_before = len(Actor.query.all())
        response = self.client().post('/actors', headers=self.casting_director, json=self.new_actor)
        data = json.loads(response.data)
        total_actors_after = total_actors_before + 1

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(total_actors_after, 1)

    def test_director_post_movies(self):
        """
        Tests casting director can create movies
        """
        response = self.client().post('/movies', headers=self.casting_director, json=self.new_movie)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    def test_director_patch_actors(self):
        """
        Tests casting director can update actor
        """
        before_update = self.client().get('/actors', headers=self.casting_director)
        before_update = json.loads(before_update.data)["actors"][0]
        update_actor = {'name': before_update["name"] + "S"}
        response = self.client().patch('/actors/24', headers=self.casting_director,
                                       json=update_actor)
        data = json.loads(response.data)
        after_update = data["actors"][0]

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(before_update, after_update, "Update successful")

    def test_director_patch_movies(self):
        """
        Tests casting director can update movies
        """
        before_update = self.client().get('/movies', headers=self.casting_director)
        before_update = json.loads(before_update.data)["movies"][0]
        update_movie = {'title': before_update["title"] + "S"}
        response = self.client().patch('/movies/10', headers=self.casting_director,
                                       json=update_movie)
        data = json.loads(response.data)
        after_update = data

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(before_update, after_update, "Update successful")

    def test_director_delete_actors(self):
        """
        Tests casting director can delete actor
        """
        response = self.client().delete('/actors/25', headers=self.casting_director)
        data = json.loads(response.data)
        actor = Actor.query.filter(Actor.id == 25).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 25)
        self.assertEqual(actor, None)

    def test_director_delete_movies(self):
        """
        Tests casting director cannot delete movies
        """
        response = self.client().delete('/movies/1', headers=self.casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Tests for casting producer
    def test_producer_get_actors(self):
        """
        Tests casting producer can view actors data
        """
        response = self.client().get('/actors', headers=self.casting_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_producer_get_movies(self):
        """
        Tests casting producer can view movies data
        """
        response = self.client().get('/movies', headers=self.casting_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_producer_post_actors(self):
        """
        Tests casting producer can create actor
        """
        total_actors_before = len(Actor.query.all())
        response = self.client().post('/actors', headers=self.casting_producer, json=self.new_actor)
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
        print("total_movies_before", total_movies_before)
        response = self.client().post('/movies', headers=self.casting_producer, json=self.new_movie)
        print("response", response)
        data = json.loads(response.data)
        print("data", data)
        total_movies_after = total_movies_before + 1
        print("total_movies_after", total_movies_after)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(total_movies_after, 1)

    def test_producer_patch_actors(self):
        """
        Tests casting producer can update actor
        """
        before_update = self.client().get('/actors', headers=self.casting_producer)
        before_update = json.loads(before_update.data)["actors"][0]
        update_actor = {'name': before_update["name"] + "S"}
        response = self.client().patch('/actors/24', headers=self.casting_producer,
                                       json=update_actor)
        data = json.loads(response.data)
        after_update = data["actors"][0]

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(before_update, after_update, "Update successful")

    def test_producer_patch_movies(self):
        """
        Tests casting producer can update movies
        """
        before_update = self.client().get('/movies', headers=self.casting_producer)
        before_update = json.loads(before_update.data)["movies"][0]
        update_movie = {'title': before_update["title"] + "S"}
        response = self.client().patch('/movies/10', headers=self.casting_producer,
                                       json=update_movie)
        data = json.loads(response.data)
        after_update = data

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(before_update, after_update, "Update successful")

    def test_producer_delete_actors(self):
        """
        Tests casting producer can delete actor
        """
        response = self.client().delete('/actors/25', headers=self.casting_producer)
        data = json.loads(response.data)
        actor = Actor.query.filter(Actor.id == 25).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 25)
        self.assertEqual(actor, None)

    def test_producer_delete_movies(self):
        """
        Tests casting producer cannot delete movies
        """
        response = self.client().delete('/movies/2', headers=self.casting_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)
        self.assertEqual(actor, None)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()